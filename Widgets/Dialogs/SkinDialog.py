#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.SkinDialog
@description: 
"""

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QButtonGroup

from UiFiles.Ui_SkinDialog import Ui_FormSkinDialog
from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog
from Widgets.Layouts.FlowLayout import FlowLayout
from Widgets.Skins.PreviewWidget import PreviewWidget
from Widgets.Skins.PictureWidget import PictureWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class SkinDialog(MoveDialog, Ui_FormSkinDialog):

    def __init__(self, *args, **kwargs):
        super(SkinDialog, self).__init__(*args, **kwargs)
        # 记录当前主题的样式表（用于后面修改背景或者颜色）
        self._oldStyleSheet = ThemeManager.styleSheet()
        self.setupUi(self)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.widgetBottom.setVisible(False)
        # 预览界面
        self.previewWidget = PreviewWidget(self.widgetSkinBg)
        self.previewWidget.setVisible(False)
        # 初始化信号槽
        self._initSignals()
        # 加载鼠标样式
        ThemeManager.loadCursor(self)
        self.on_tabWidgetSkinMain_currentChanged(0)

    def _initSignals(self):
        Signals.pictureItemAdded.connect(self.onPictureItemAdded)
        Signals.pictureDownFinished.connect(self.onPictureDownFinished)
        # 点击某个主题
        Signals.themeItemClicked.connect(self.onThemeItemClicked)
        # 点击颜色
        Signals.colourfulItemClicked.connect(self.onColourfulItemClicked)
        # 点击图片
        Signals.pictureItemClicked.connect(self.onPictureItemClicked)

    def onThemeItemClicked(self, name, path):
        """
        :param name:        主题名字
        :param path:        主题预览图路径
        """
        self.previewWidget.setVisible(True)
        self.previewWidget.setTitle(name)
        self.previewWidget.setPixmap(
            QPixmap(path).scaledToWidth(400, Qt.SmoothTransformation))

    def onColourfulItemClicked(self, name, color):
        """
        :param name:        颜色名字
        :param color:       颜色
        """

    def onPictureItemClicked(self, name, path):
        """
        :param name:        壁纸名字
        :param path:        壁纸路径
        """
        self.previewWidget.setVisible(True)
        self.previewWidget.setTitle(name)
        self.previewWidget.setPixmap(
            QPixmap(path).scaledToHeight(385, Qt.SmoothTransformation))

    def on_tabWidgetSkinMain_currentChanged(self, index):
        """tab标签切换"""
        w = self.tabWidgetSkinMain.widget(index)
        if w == self.tabPicture:
            if self.stackedWidgetPictures.count() > 0:
                return
            self.initCategories()
        else:
            w.init()

    def initCategories(self):
        """添加分类标签页
        :param categories:        分类
        """
        self.categoryLayout = FlowLayout(self.widgetCategories)
        self.categoryLayout.setSpacing(10)
        self.categoryBtnGroups = QButtonGroup(self)
        self.categoryBtnGroups.buttonToggled.connect(self.onCategoryChanged)
        for category in ('4K', '双屏', '美女', '动漫', '风景', '明星', '萌宠', '游戏', '科技', '其他'):
            button = QPushButton(category, self.widgetCategories)
            button.setCheckable(True)
            self.categoryBtnGroups.addButton(button)
            self.categoryLayout.addWidget(button)
            widget = PictureWidget(category, self.stackedWidgetPictures)
            button.setProperty('widget', widget)
            self.stackedWidgetPictures.addWidget(widget)
        self.categoryBtnGroups.buttons()[0].setChecked(True)

    def onCategoryChanged(self, button, toggled):
        """分类切换
        :param button:        分类按钮
        :param toggled:       是否选中
        """
        if not toggled:
            return
        widget = button.property('widget')
        self.stackedWidgetPictures.setCurrentWidget(widget)
        runnable = widget.init()
        if runnable:
            if not hasattr(self, '_threadPool'):
                self._threadPool = QThreadPool(self)
                self._threadPool.setMaxThreadCount(5)
            widget.showWaiting()
            self._threadPool.start(runnable)

    def onPictureDownFinished(self, widget):
        widget.showWaiting(False)

    def onPictureItemAdded(self, widget, index, title, path):
        """添加分类图片Item
        :param widget:            该分类对应的PictureWidget
        :param index:             序号
        :param title:             标题
        :param path:              图片路径
        """
        widget.addItem(index, title, path)

    def showEvent(self, event):
        super(SkinDialog, self).showEvent(event)
        self.previewWidget.setGeometry(self.widgetSkinBg.rect())

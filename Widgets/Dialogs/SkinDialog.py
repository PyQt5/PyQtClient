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
from PyQt5.QtWidgets import QPushButton, QButtonGroup

from UiFiles.Ui_SkinDialog import Ui_FormSkinDialog
from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager
from Utils.ThemeThread import GetAllCategoriesRunnable
from Widgets.Dialogs.MoveDialog import MoveDialog
from Widgets.Layouts.FlowLayout import FlowLayout
from Widgets.Skins.PictureWidget import PictureWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class SkinDialog(MoveDialog, Ui_FormSkinDialog):

    def __init__(self, *args, **kwargs):
        super(SkinDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.widgetBottom.setVisible(False)
        # 背景图片面板
        Signals.getCategoriesFinished.connect(self.onGetCategoriesFinished)
        Signals.getCategoryFinished.connect(self.onGetCategoryFinished)
        Signals.pictureDownloadFinished.connect(self.onPictureDownloadFinished)
        self.categoryLayout = FlowLayout(self.widgetCategories)
        self.categoryLayout.setSpacing(20)
        # 加载鼠标样式
        ThemeManager.loadCursor(self)
        self.on_tabWidgetSkinMain_currentChanged(0)

    def on_tabWidgetSkinMain_currentChanged(self, index):
        """tab标签切换"""
        w = self.tabWidgetSkinMain.widget(index)
        if w == self.tabPicture:
            if self.stackedWidgetPictures.count() > 0:
                return
            QThreadPool.globalInstance().start(GetAllCategoriesRunnable())
        else:
            w.init()

    def onGetCategoriesFinished(self, categories):
        """添加分类标签页
        :param categories:        分类
        """
        self.categoryBtnGroups = QButtonGroup(self)
        self.categoryBtnGroups.buttonToggled.connect(self.onCategoryChanged)
        for category in categories:
            button = QPushButton(category.get(
                'name', '未知'), self.widgetCategories)
            button.setCheckable(True)
            self.categoryBtnGroups.addButton(button)
            self.categoryLayout.addWidget(button)
            self.stackedWidgetPictures.addWidget(
                PictureWidget(category.get('id', '36'), self.stackedWidgetPictures))
        self.categoryBtnGroups.buttons()[0].setChecked(True)

    def onCategoryChanged(self, button, toggled):
        """分类切换
        :param button:        分类按钮
        :param toggled:       是否选中
        """
        if not toggled:
            return
        index = self.categoryBtnGroups.id(button)
        self.stackedWidgetPictures.setCurrentIndex(index)
        self.stackedWidgetPictures.widget(index).init()

    def onGetCategoryFinished(self, widget, items):
        """某个分类json下载完成
        :param widget:            该分类对应的PictureWidget
        :param items:             分类中的数组
        """
        widget.setItems(items)

    def onPictureDownloadFinished(self, widget, index, path):
        """分类图片下载完成
        :param widget:            该分类对应的PictureWidget
        :param index:             序号
        :param path:              图片路径
        """
        widget.addItem(index, path)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月30日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.PreviewWidget
@description: 主题预览
"""
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect

from UiFiles.Ui_PreviewWidget import Ui_FormPreviewWidget
from Utils.ThemeManager import ThemeManager


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class PreviewWidget(QWidget, Ui_FormPreviewWidget):

    def __init__(self, *args, **kwargs):
        super(PreviewWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 支持样式
        # 图片边缘阴影效果
        effect = QGraphicsDropShadowEffect(self.labelPreviewImage)
        effect.setBlurRadius(40)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.labelPreviewImage.setGraphicsEffect(effect)
        # 鼠标样式
        ThemeManager.loadCursor(self, ThemeManager.CursorDefault)
        ThemeManager.loadCursor(self.buttonPreviewApply,
                                ThemeManager.CursorPointer)
        ThemeManager.loadCursor(self.buttonPreviewClose,
                                ThemeManager.CursorPointer)
        ThemeManager.loadCursor(self.buttonPreviewNext,
                                ThemeManager.CursorPointer)
        ThemeManager.loadCursor(
            self.buttonPreviewPrevious, ThemeManager.CursorPointer)

    def setTitle(self, title):
        """设置标题
        :param title:
        """
        self.labelPreviewTitle.setText(title)
        self.setWindowTitle(title)

    def setPixmap(self, pixmap):
        """设置图片
        :param pixmap:
        """
        self.labelPreviewImage.setPixmap(pixmap)

    @pyqtSlot()
    def on_buttonPreviewClose_clicked(self):
        """隐藏自己
        """
        self.setVisible(False)

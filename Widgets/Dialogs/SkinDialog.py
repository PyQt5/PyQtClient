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
from PyQt5.QtCore import Qt

from Widgets.Dialogs.MoveDialog import MoveDialog
from UiFiles.Ui_SkinDialog import Ui_FormSkinDialog
from Utils.ThemeManager import ThemeManager


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class SkinDialog(MoveDialog, Ui_FormSkinDialog):

    def __init__(self, *args, **kwargs):
        super(SkinDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 背景透明
#         self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
#         self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 加载鼠标样式
        ThemeManager.loadCursor(self)

    def on_tabWidget_currentChanged(self, index):
        self.tabWidget.widget(index).init()

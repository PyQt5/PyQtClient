#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月26日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Dialogs.IssuesDialog
@description: 反馈对话框
"""
from PyQt5.QtCore import Qt

from UiFiles.Ui_IssuesDialog import Ui_FormIssuesDialog
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class IssuesDialog(MoveDialog, Ui_FormIssuesDialog):

    def __init__(self, *args, **kwargs):
        super(IssuesDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 关闭后自动销毁
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 加载鼠标样式
        ThemeManager.loadCursor(self)

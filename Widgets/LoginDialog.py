#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.LoginDialog
@description:
"""
from PyQt5.QtCore import Qt, pyqtSlot

from UiFiles.Ui_LoginDialog import Ui_FormLoginDialog
from Widgets.MoveDialog import MoveDialog
from Widgets.TwinkleDialog import TwinkleDialog

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class LoginDialog(MoveDialog, TwinkleDialog, Ui_FormLoginDialog):

    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 设置闪烁的目标控件
        self.setTarget(self.widgetLogin)
        # 关闭后自动销毁
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    @pyqtSlot()
    def on_buttonLogin_clicked(self):
        # 登录点击
        account = self.lineEditAccount.text().strip()
        password = self.lineEditPassword.text().strip()
        if not account:
            self.labelNotice(self.tr('Incorrect account'))
            return
        if not password:
            self.labelNotice(self.tr('Incorrect password'))
            return
        self.labelNotice.setText('')

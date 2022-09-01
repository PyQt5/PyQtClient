#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Dialogs.LoginDialog
@description: 登录对话框
"""

import os

from PyQt5.QtCore import Qt, QTimer, QVariant, pyqtSlot
from PyQt5.QtWidgets import QCompleter
from UiFiles.Ui_LoginDialog import Ui_FormLoginDialog
from Utils import Constants
from Utils.CommonUtil import AppLog, Setting, Signals, get_avatar_path
from Utils.GitThread import LoginThread
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.MoveDialog import MoveDialog
from Widgets.Dialogs.TwinkleDialog import TwinkleDialog


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
        # 加载鼠标样式
        ThemeManager.loadCursor(self)
        # 加载鼠标样式
        ThemeManager.loadCursor(self.buttonHead, ThemeManager.CursorPointer)
        # 是否正在登录
        self._isLogin = False
        Signals.loginErrored.connect(self.onLoginErrored)
        Signals.loginSuccessed.connect(self.onLoginSuccessed)
        QTimer.singleShot(200, self.initAccount)

    def initAccount(self):
        # 自动填充账号密码
        self._accounts = Setting.value('accounts', {}, QVariant)
        completer = QCompleter(self._accounts.keys(), self.lineEditAccount)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        # 在内部自动填充完成
        completer.setCompletionMode(QCompleter.InlineCompletion)
        # 设置objectName用于设置样式
        # completer.popup().setObjectName('lineEditAccountAuto')
        self.lineEditAccount.setCompleter(completer)

        # 读取储存的账号密码
        account = Setting.value('account', '', str)
        self.lineEditAccount.setText(account)

    def on_lineEditAccount_textChanged(self, account):
        """输入框编辑完成信号,寻找头像文件是否存在
        """
        if account not in self._accounts:  # 不存在
            return
        # 更新头像
        path = get_avatar_path(account)
        if os.path.exists(path) and self.buttonHead.image != path:
            # 更换头像
            self.buttonHead.image = path

    def onLoginErrored(self, message):
        AppLog.debug('onLoginErrored')
        self._isLogin = False
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        AppLog.error(message)
        if message:
            self.labelNotice.setText(message)

    def onLoginSuccessed(self, account, status, emoji):
        AppLog.debug('onLoginSuccessed')
        self._isLogin = False
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        # 用账号密码实例化github访问对象
        account = self.lineEditAccount.text().strip()
        Constants._Account = account
        Constants._Username = account
        Constants._Status = status
        Constants._Emoji = emoji
        # 储存账号密码
        Setting.setValue('account', account)
        if account in self._accounts:
            _, s, e = self._accounts[account]
            status = status or s
            emoji = emoji or e
        # 更新账号数组
        self._accounts[account] = [account, status, emoji]
        Setting.setValue('accounts', self._accounts)
        self.accept()

    def setEnabled(self, enabled):
        self.buttonClose.setEnabled(enabled)
        self.lineEditAccount.setEnabled(enabled)
        self.buttonLogin.setEnabled(enabled)

    @pyqtSlot()
    def on_buttonLogin_clicked(self):
        # 登录点击
        account = self.lineEditAccount.text().strip()
        if not account:
            self.labelNotice.setText(self.tr('Incorrect account'))
            return
        self.labelNotice.setText('')
        self.setEnabled(False)
        self.buttonLogin.showWaiting(True)
        LoginThread.start(account, '')

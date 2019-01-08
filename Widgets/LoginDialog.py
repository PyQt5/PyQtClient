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
import base64

from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from github import Github

from UiFiles.Ui_LoginDialog import Ui_FormLoginDialog
from Utils import Constants
from Utils.CommonUtil import AppLog, Setting
from Utils.ThemeManager import ThemeManager
from Widgets.MoveDialog import MoveDialog
from Widgets.TwinkleDialog import TwinkleDialog


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class LoginThread(QThread):

    loginErrored = pyqtSignal(str, str)
    loginSuccessed = pyqtSignal()

    def __init__(self, account, password, *args, **kwargs):
        super(LoginThread, self).__init__(*args, **kwargs)
        self.account = account
        self.password = password

    def run(self):
        try:
            g = Github(self.account, self.password)
            user = g.get_user()
            if user.login:
                # 登录成功
                self.loginSuccessed.emit()
        except Exception as e:
            self.loginErrored.emit(
                str(e), self.tr('Incorrect account or password'))


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
        # 登录线程
        self._loginThread = None
        # 自动填充账号密码
        self.lineEditAccount.setText(Setting.value('account', '', str))
        try:
            self.lineEditPassword.setText(base64.b85decode(
                Setting.value('password', '', str).encode()).decode())
        except Exception as e:
            self.lineEditPassword.setText('')
            AppLog.warn(str(e))

    def onLoginStarted(self):
        AppLog.debug('onLoginStarted')

    def onLoginFinished(self):
        AppLog.debug('onLoginFinished')
        # 储存账号密码
        Setting.setValue('account', self.lineEditAccount.text().strip())
        Setting.setValue('password', base64.b85encode(
            self.lineEditPassword.text().strip().encode()).decode())
        self.closeThread()
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        self.accept()

    def onLoginErrored(self, e, message):
        AppLog.debug('onLoginErrored')
        self.closeThread()
        AppLog.error(e)
        AppLog.error(message)
        if message:
            self.labelNotice.setText(message)

    def onLoginSuccessed(self):
        AppLog.debug('onLoginSuccessed')
        self.closeThread()
        # 登录成功保存账号和密码
        Constants._Github = Github(self.lineEditAccount.text(
        ).strip(), self.lineEditPassword.text().strip())

    def closeThread(self):
        # 关闭线程
        if self._loginThread:
            self._loginThread.quit()
            self._loginThread.deleteLater()
            self._loginThread = None

    def setEnabled(self, enabled):
        self.buttonClose.setEnabled(enabled)
        self.lineEditAccount.setEnabled(enabled)
        self.lineEditPassword.setEnabled(enabled)
        self.buttonLogin.setEnabled(enabled)

    def closeEvent(self, event):
        self.closeThread()
        super(LoginDialog, self).closeEvent(event)

    @pyqtSlot()
    def on_buttonLogin_clicked(self):
        # 登录点击
        account = self.lineEditAccount.text().strip()
        password = self.lineEditPassword.text().strip()
        if not account:
            self.labelNotice.setText(self.tr('Incorrect account'))
            return
        if not password:
            self.labelNotice.setText(self.tr('Incorrect password'))
            return
        self.labelNotice.setText('')
        self.setEnabled(False)
        self.buttonLogin.showWaiting(True)
        self._loginThread = LoginThread(account, password, self)
        # 绑定信号槽
        self._loginThread.started.connect(self.onLoginStarted)
        self._loginThread.finished.connect(self.onLoginFinished)
        self._loginThread.loginErrored.connect(self.onLoginErrored)
        self._loginThread.loginSuccessed.connect(self.onLoginSuccessed)
        self._loginThread.start()

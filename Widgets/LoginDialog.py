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
import os

from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal, QVariant, QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QCompleter
from github import Github
import requests

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
    loginSuccessed = pyqtSignal(int)  # 登录成功发送用户的id

    def __init__(self, account, password, *args, **kwargs):
        super(LoginThread, self).__init__(*args, **kwargs)
        self.account = account
        self.password = password

    def run(self):
        try:
            g = Github(self.account, self.password)
            user = g.get_user()
            if user.login:
                AppLog.info('login: {}'.format(user.login))
                # 获取头像
                req = requests.get(user.avatar_url)
                if req.status_code == 200:
                    imgformat = req.headers.get(
                        'content-type', 'image/jpg').split('/')[1]
                    Constants.ImageAvatar = os.path.join(
                        Constants.ImageDir, str(user.id)).replace('\\', '/') + '.jpg'
                    AppLog.debug('image type: {}'.format(imgformat))
                    AppLog.debug('content length: {}'.format(len(req.content)))

                    image = QImage()
                    if image.loadFromData(req.content):
                        # 缩放图片
                        if not image.isNull():
                            image = image.scaled(130, 130, Qt.IgnoreAspectRatio,
                                                 Qt.SmoothTransformation)
                            AppLog.debug('save to: {}'.format(
                                Constants.ImageAvatar))
                            image.save(Constants.ImageAvatar)
                        else:
                            AppLog.warn('avatar image is null')
                    else:
                        AppLog.warn('can not load from image data')
                # 登录成功
                self.loginSuccessed.emit(user.id)
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
        # 加载鼠标样式
        ThemeManager.loadCursor(self.buttonHead,'pointer.png')
        # 登录线程
        self._loginThread = None
        QTimer.singleShot(100, self.initAccount)

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
        # 填充密码
        try:
            self.lineEditPassword.setText(base64.b85decode(
                self._accounts[account][1].encode()).decode())
        except Exception as e:
            self.lineEditPassword.setText('')
            AppLog.warn(str(e))
        # 更新头像
        path = os.path.join(Constants.ImageDir, self._accounts[account][0]).replace(
            '\\', '/') + '.jpg'
        if os.path.exists(path) and self.buttonHead.image != path:
            # 更换头像
            self.buttonHead.image = path

    def onLoginStarted(self):
        AppLog.debug('onLoginStarted')

    def onLoginFinished(self):
        AppLog.debug('onLoginFinished')
        self.closeThread()
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)

    def onLoginErrored(self, e, message):
        AppLog.debug('onLoginErrored')
        self.closeThread()
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        AppLog.error(e)
        AppLog.error(message)
        if message:
            self.labelNotice.setText(message)

    def onLoginSuccessed(self, uid):
        AppLog.debug('onLoginSuccessed')
        self.closeThread()
        self.buttonLogin.showWaiting(False)
        self.setEnabled(True)
        # 用账号密码实例化github访问对象
        account = self.lineEditAccount.text().strip()
        password = self.lineEditPassword.text().strip()
        Constants._Github = Github(account, password)
        # 储存账号密码
        Setting.setValue('account', account)
        if account not in self._accounts:
            # 更新账号数组
            self._accounts[account] = [
                str(uid), base64.b85encode(password.encode()).decode()]
            Setting.setValue('accounts', self._accounts)
        self.accept()

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

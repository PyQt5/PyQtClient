#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.GitThread
@description: Git操作线程
"""
import os

from PyQt5.QtCore import Qt, QCoreApplication, QThread, QObject
from PyQt5.QtGui import QImage
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectTimeout

from Utils import Constants
from Utils.CommonUtil import Signals, AppLog


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class LoginThread(QObject):
    """登录Github,获取头像和项目最新的sha值
    """

    Url = 'https://api.github.com/user'

    def __init__(self, account, password, *args, **kwargs):
        super(LoginThread, self).__init__(*args, **kwargs)
        self.account = account
        self.password = password

    @classmethod
    def start(cls, account, password, parent=None):
        """启动登录线程
        :param cls:
        :param account:        账号
        :param password:       密码
        """
        cls._thread = QThread(parent)
        cls._worker = LoginThread(account, password)
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('login thread started')

    def run(self):
        AppLog.info('start login github')
        try:
            req = requests.get(self.Url, auth=HTTPBasicAuth(
                self.account, self.password))
            retval = req.json()
            if retval.get('message', '') == 'Bad credentials':
                Signals.loginErrored.emit(QCoreApplication.translate(
                    'Repository', 'Incorrect account or password'))
                AppLog.warn('Incorrect account or password')
                return
            if 'login' not in retval:
                Signals.loginErrored.emit(QCoreApplication.translate(
                    'Repository', 'Login failed, Unknown reason'))
                AppLog.warn('Login failed, Unknown reason')
                return
            # 用户ID
            uid = retval.get('id', 0)
            AppLog.debug('user id: {}'.format(uid))
            # 用户昵称
            name = retval.get('name', 'Unknown')
            AppLog.debug('user name: {}'.format(name))
            # 用户头像地址
            avatar_url = retval.get('avatar_url', '')
            if avatar_url:
                # 获取头像
                try:
                    req = requests.get(avatar_url)
                    if req.status_code == 200:
                        imgformat = req.headers.get(
                            'content-type', 'image/jpg').split('/')[1]
                        Constants.ImageAvatar = os.path.join(
                            Constants.ImageDir, str(uid)).replace('\\', '/') + '.jpg'
                        AppLog.debug('image type: {}'.format(imgformat))
                        AppLog.debug(
                            'content length: {}'.format(len(req.content)))

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
                except Exception as e:
                    AppLog.warn(str(e))
            Signals.loginSuccessed.emit(str(uid), name)
        except ConnectTimeout as e:
            Signals.loginErrored.emit(QCoreApplication.translate(
                'Repository', 'Connect Timeout'))
            AppLog.warn(str(e))
        except ConnectionError as e:
            Signals.loginErrored.emit(QCoreApplication.translate(
                'Repository', 'Connection Error'))
            AppLog.warn(str(e))
        except Exception as e:
            Signals.loginErrored.emit(QCoreApplication.translate(
                'Repository', 'Unknown Error'))
            AppLog.warn(str(e))
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.Repository
@description: 仓库下载
"""
import os

from PyQt5.QtCore import QRunnable, Qt, QCoreApplication
from PyQt5.QtGui import QImage
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectTimeout

from Utils import Constants
from Utils.CommonUtil import git_blob_hash, Signals, AppLog


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class LoginRunnable(QRunnable):
    """登录Github
    """

    Url = 'https://api.github.com/user'

    def __init__(self, account, password, *args, **kwargs):
        super(LoginRunnable, self).__init__(*args, **kwargs)
        self.account = account
        self.password = password

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


class DirRunnable(QRunnable):
    """获指定路径下的目录和文件
    """

    Url = 'https://api.github.com/repos/PyQt5/PyQt/contents'

    def __init__(self, path, account, password, *args, **kwargs):
        super(DirRunnable, self).__init__(*args, **kwargs)
        # 如果path == '' 则表示获取根目录,不用递归获取
        self.path = path
        self.account = account
        self.password = password

    def _analysis(self, retval, isRoot=False):
        """解析josn数组
        :param retval:    数组
        """
        AppLog.debug('retval length: {}, isRoot: {}'.format(
            len(retval), isRoot))
        for item in retval:
            name = item['name']
            rpath = item['path']
            type_ = item['type']
            path = os.path.join(Constants.DirProjects,
                                rpath).replace('\\', '/')
            AppLog.debug('name: {}, type: {}'.format(name, type_))
            if type_ == 'dir':  # 目录
                # 尝试创建目录
                try:
                    os.makedirs(path, exist_ok=True)
                    if path.startswith('.'):  # 忽略.开头的目录
                        continue
                    if isRoot:
                        # 添加到界面树中
                        pass
                    if name == 'Donate' or not isRoot:
                        # 继续遍历
                        self.getContent('/' + rpath)
                except Exception as e:
                    AppLog.warn(str(e))
            elif type_ == 'file':  # 文件
                sha = item['sha']
                # 如果文件不存在或者sha不一致则重新写入
                if not os.path.exists(path) or sha != git_blob_hash(path):
                    AppLog.debug('overwrite file: {}'.format(path))
                    Signals.fileDownloaded.emit(path, item['download_url'])

    def getContent(self, path):
        AppLog.info('start get {} catalogs'.format(path))
        try:
            req = requests.get(self.Url + path, auth=HTTPBasicAuth(
                self.account, self.password))
            retval = req.json()
            if isinstance(retval, dict):
                AppLog.warn('Not Found')
                return
            self._analysis(retval, path == '')
        except Exception as e:
            AppLog.warn(str(e))

    def run(self):
        path = '/' + self.path if self.path else ''
        self.getContent(path)
        Signals.DirDownloadFinished.emit(self.path if self.path else '/')
        AppLog.debug('Download dir end: {}'.format(self.path))


class DownloadRunnable(QRunnable):
    """文件下载
    """

    def __init__(self, path, url, *args, **kwargs):
        super(DownloadRunnable, self).__init__(*args, **kwargs)
        self.path = path
        self.url = url

    def run(self):
        try:
            req = requests.get(self.url)
            with open(self.path, 'wb') as fp:
                fp.write(req.content)
        except Exception as e:
            AppLog.warn(str(e))
        AppLog.debug('download file end: {}'.format(self.url))
        Signals.fileDownloadFinished.emit(self.path)

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
from collections import OrderedDict
import os

from PyQt5.QtCore import QRunnable, Qt, QCoreApplication, QThread
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


class LoginRunnable(QRunnable):
    """登录Github
    """

    Url = 'https://api.github.com/user'

    def __init__(self, account, password, *args, **kwargs):
        super(LoginRunnable, self).__init__(*args, **kwargs)
        self.setAutoDelete(True)
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


class TreesRunnable(QRunnable):
    """获取目录树
    """

    Url = 'https://api.github.com/repos/PyQt5/PyQt/git/trees/master?recursive=1'

    def __init__(self, account, password, *args, **kwargs):
        super(TreesRunnable, self).__init__(*args, **kwargs)
        self.setAutoDelete(True)
        self.account = account
        self.password = password

    def run(self):
        AppLog.info('start get github trees')
        try:
            req = requests.get(self.Url)
            trees = req.json()['tree']
            RepositoryTrees = OrderedDict()
            RepositoryTrees['/'] = []
            for tree in trees:
                path = tree['path']
                if path.startswith('.'):
                    # .开头的文件或目录跳过
                    continue
                # 根目录下的文件
                if path.count('/') == 0 and tree['type'] == 'blob':
                    RepositoryTrees['/'].append(tree)
                    continue
                # 提取整理所有根节点下的目录和文件
                name = path.split('/')[0]
                if name not in RepositoryTrees:
                    RepositoryTrees[name] = []
                else:
                    # 添加非目录
                    if tree['type'] != 'tree':
                        RepositoryTrees[name].append(tree)
            Signals.treesFinished.emit(RepositoryTrees)
        except Exception as e:
            Signals.errorShowed.emit(QCoreApplication.translate(
                'Repository', 'Get Trees Error: {}'.format(str(e))))
            AppLog.warn(str(e))
        Signals.runnableFinished.emit('/')


class DirRunnable(QRunnable):
    """获指定路径下的目录和文件
    """

    Url = 'https://raw.githubusercontent.com/PyQt5/PyQt/master/'

    def __init__(self, name, item, values, account, password, *args, **kwargs):
        """
        :param name:            QRunnable名字
        :param item:            上级item
        :param values:          子目录数组
        :param account:         账号
        :param password:        密码
        """
        super(DirRunnable, self).__init__(*args, **kwargs)
        self.setAutoDelete(True)
        self.name = name
        self.item = item
        self.values = values
        self.account = account
        self.password = password

    def run(self):
        for index, value in enumerate(self.values):
            # 远程路径
            rPath = value['path']
            # 本地路径
            lPath = os.path.join(Constants.DirProjects,
                                 rPath).replace('\\', '/')
#             sha = value['sha']
            size = value['size']
            # 创建目录
            os.makedirs(os.path.dirname(lPath), exist_ok=True)
            # 如果文件不存在或者sha不一致则重新写入
#             if not os.path.isfile(lPath) or sha != git_blob_hash(lPath):
            # 不考虑sha, 粗略的采用文件大小比较
            if not os.path.isfile(lPath) or size != os.path.getsize(lPath):
                try:
                    req = requests.get(self.Url + value['path'], auth=HTTPBasicAuth(
                        self.account, self.password))
                    with open(lPath, 'wb') as fp:
                        fp.write(req.content)
                    AppLog.debug('overwrite file: {}'.format(lPath))

                    # 如果只有一个/并且后缀是.py则通知添加到item中
                    if rPath.count('/') == 1 and rPath[-3:] == '.py':
                        Signals.childItemAdded.emit(self.item, lPath)
                except Exception as e:
                    AppLog.debug(
                        'overwrite file {} failed'.format(str(e), lPath))
            # 更新进度条
            Signals.itemProgressChanged.emit(self.item, index + 1)
        AppLog.debug('Download dir end: {}'.format(self.name))
        Signals.runnableFinished.emit(self.name)
        QThread.msleep(200)
        QThread.yieldCurrentThread()

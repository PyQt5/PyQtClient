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
from Utils.Constants import ProjectRepo, DirProjects


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class LoginRunnable(QRunnable):
    """登录Github
    """

    def __init__(self, account, password, *args, **kwargs):
        super(LoginRunnable, self).__init__(*args, **kwargs)
        self.account = account
        self.password = password

    def run(self):
        AppLog.info('start login github')
        try:
            req = requests.get('https://api.github.com/user',
                               auth=HTTPBasicAuth(self.account, self.password))
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

    def __init__(self, path, account, password, *args, **kwargs):
        super(DirRunnable, self).__init__(*args, **kwargs)
        # 如果path == '' 则表示获取根目录,不用递归获取
        self.path = path
        self.account = account
        self.password = password

    def run(self):
        path = '/' + self.path if self.path else ''
        req = requests.get('https://api.github.com/repos/PyQt5/PyQt/contents' + path,
                           auth=HTTPBasicAuth(self.account, self.password))
        print(req.json())
        AppLog.info('start get {} catalogs'.format(self.path))
        repo = Constants._Github.get_repo(ProjectRepo)
        contents = repo.get_contents(self.path)
        while len(contents) > 0:
            content = contents.pop(0)
            if content.type == 'dir':
                # 尝试创建目录
                try:
                    os.makedirs(os.path.join(
                        DirProjects, content.path).replace('\\', '/'), exist_ok=True)
                    if not content.path.startswith('.'):  # 文件名不以.开头
                        # 添加到界面树中
                        Signals.itemAdded.emit(
                            content.path.split('/'), content.path)
                        if content.name == 'Donate':  # 继续遍历
                            contents.extend(repo.get_contents(content.path))
                        # 是否需要深度遍历
                        if self.path != '':
                            AppLog.info(
                                'start get {} catalogs'.format(content.path))
                            contents.extend(repo.get_contents(content.path))
                except Exception as e:
                    AppLog.warn(str(e))
            else:
                path = os.path.join(
                    DirProjects, content.path).replace('\\', '/')
                # 如果文件不存在或者sha不一致则重新写入
                if not os.path.exists(path) or content.sha != git_blob_hash(path):
                    AppLog.debug('overwrite file: {}'.format(path))
                    with open(path, 'wb') as fp:
                        fp.write(content.decoded_content)
                # 判断文件名是否是README
                if content.name == 'README.md':
                    # 通知是否要更新右侧内容显示
                    Signals.indexPageUpdated.emit()

        Signals.runnableFinished.emit(self.path)

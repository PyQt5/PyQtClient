#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Utils.GitThread
@description: Git操作线程
"""

import os
import re
import shutil
import stat
from contextlib import closing
from pathlib import Path
from time import time
from zipfile import ZipFile

import pygit2
import requests
from PyQt5.QtCore import QCoreApplication, QObject, Qt, QThread
from PyQt5.QtGui import QImage
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectTimeout

from Utils import Constants, Version
from Utils.CommonUtil import AppLog, Signals, get_avatar_path


class LoginThread(QObject):
    """登录Github,获取头像
    """

    Url = 'https://github.com/{0}.png?size=130'

    def __init__(self, account, password, *args, **kwargs):
        super(LoginThread, self).__init__(*args, **kwargs)
        self.account = account
        self.password = password
        self.status = ''
        self.emoji = ''

    @classmethod
    def quit(cls):
        """退出线程
        :param cls:
        """
        if hasattr(cls, '_thread'):
            cls._thread.quit()
            AppLog.info('login thread quit')

    @classmethod
    def start(cls, account, password='', parent=None):
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

    def save_avatar(self, data):
        """保存头像
        :param data: 头像数据
        """
        Constants.ImageAvatar = get_avatar_path(self.account)
        image = QImage()
        if image.loadFromData(data):
            # 缩放图片
            if not image.isNull():
                if image.width() != 130 or image.height() != 130:
                    AppLog.warn('scaled avatar image size to 130x130')
                    image = image.scaled(130, 130, Qt.IgnoreAspectRatio,
                                         Qt.SmoothTransformation)
                AppLog.debug('save to: {}'.format(Constants.ImageAvatar))
                return image.save(Constants.ImageAvatar)
            else:
                AppLog.warn('avatar image is null')
        else:
            AppLog.warn('can not load from image data')
        return False

    def get_avatar(self, url):
        """获取头像
        :param url: 头像url
        """
        try:
            req = requests.get(url)
            if req.status_code == 200 and req.headers.get(
                    'Content-Type').startswith('image/'):
                imgformat = req.headers.get('Content-Type', '').split('/')[-1]
                AppLog.debug('image type: {}'.format(imgformat))
                AppLog.debug('content length: {}'.format(len(req.content)))
                return self.save_avatar(req.content)
        except Exception as e:
            AppLog.warning(str(e))
        return False

    def run(self):
        AppLog.info('start login github')

        # 方式一从url直接获取
        av_ok = self.get_avatar(self.Url.format(self.account))

        # 方式二从网页提取
        try:
            req = requests.get(
                self.Url.format(self.account).split('.png?size')[0])
            if req.status_code == 200:
                # 获取头像url
                aurls = re.findall(
                    r'<meta property="og:image"\s*content="(.*?)"\s*/>'.encode(
                    ), req.content)
                # 获取状态
                status = re.findall(
                    r'<div class="user-status-message-wrapper.*?"\s*>\s*<div>\s*(.*?)\s*</div>'
                    .encode(), req.content)
                if status:
                    self.status = status[0].decode()
                # 获取状态图标
                emoji = re.findall(
                    r'<g-emoji.*?fallback-src="(.*?)"\s*>(.*?)</g-emoji>'.
                    encode(), req.content)
                if emoji:
                    self.emoji = emoji[0][-1].decode()
                    if self.emoji.startswith('http'):
                        self.emoji = ''
                # 下载头像
                if not av_ok and len(aurls) > 0:
                    av_ok = self.get_avatar(aurls[0])
        except Exception as e:
            AppLog.warning(str(e))

        if av_ok:
            Signals.loginSuccessed.emit(self.account, self.status, self.emoji)
        else:
            Signals.loginErrored.emit(
                QCoreApplication.translate('Repository',
                                           'Login failed, Unknown reason'))

        AppLog.info('login thread end')
        LoginThread.quit()


class ProgressCallback(pygit2.RemoteCallbacks):
    """clone过程中的进度条
    """

    def transfer_progress(self, stats):
        Signals.progressUpdated.emit(stats.received_objects,
                                     stats.total_objects)
        AppLog.debug('total: {}, received: {}'.format(stats.total_objects,
                                                      stats.received_objects))


class CloneThread(QObject):
    """获取项目源码
    """

    UrlGithub = 'https://github.com/PyQt5/PyQt.git'
    UrlGitee = 'https://gitee.com/PyQt5/PyQt.git'

    @classmethod
    def quit(cls):
        """退出线程
        :param cls:
        """
        if hasattr(cls, '_thread'):
            cls._thread.quit()
            AppLog.info('clone thread quit')

    @classmethod
    def start(cls, parent=None):
        """启动Clone线程
        :param cls:
        """
        cls._thread = QThread(parent)
        cls._worker = CloneThread()
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('clone thread started')

    def pull(self, repo, remote_name='github,gitee', branch='master'):
        """ pull changes for the specified remote (defaults to origin).

        Code from MichaelBoselowitz at:
        https://github.com/MichaelBoselowitz/pygit2-examples/blob/
            68e889e50a592d30ab4105a2e7b9f28fac7324c8/examples.py#L58
        licensed under the MIT license.
        """
        repo.remotes.set_url('gitee', self.UrlGitee)
        repo.remotes.set_url('github', self.UrlGithub)
        for remote in repo.remotes:
            if remote.name in remote_name:
                AppLog.info('update from: {}'.format(remote.name))
                remote.fetch()
                remote_master_id = repo.lookup_reference(
                    'refs/remotes/origin/%s' % (branch)).target
                merge_result, _ = repo.merge_analysis(remote_master_id)
                # Up to date, do nothing
                if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                    return
                # We can just fastforward
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                    repo.checkout_tree(repo.get(remote_master_id))
                    try:
                        master_ref = repo.lookup_reference('refs/heads/%s' %
                                                           (branch))
                        master_ref.set_target(remote_master_id)
                    except KeyError:
                        repo.create_branch(branch, repo.get(remote_master_id))
                    repo.head.set_target(remote_master_id)
                    return
                elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                    repo.merge(remote_master_id)

                    if repo.index.conflicts is not None:
                        for conflict in repo.index.conflicts:
                            for c in conflict:
                                if not c:
                                    continue
                                AppLog.error('Conflicts found in: %s', c.path)
                        raise AssertionError('Conflicts, ahhhhh!!')

                    user = repo.default_signature
                    tree = repo.index.write_tree()
                    repo.create_commit('HEAD', user, user, 'Merge!', tree,
                                       [repo.head.target, remote_master_id])
                    # We need to do this or git CLI will think we are still
                    # merging.
                    repo.state_cleanup()
                    return
                else:
                    raise AssertionError('Unknown merge analysis result')

    def remove(self):
        """删除未clone完成的目录"""
        for path in Path(Constants.DirProjects).rglob('*'):
            path.chmod(stat.S_IWRITE)
        shutil.rmtree(Constants.DirProjects, ignore_errors=True)

    def clone(self, url):
        """克隆项目"""
        AppLog.info('clone from: {}'.format(url))
        pygit2.clone_repository(url,
                                Constants.DirProjects,
                                callbacks=ProgressCallback())

    def _clone(self):
        ok = False
        for url in (self.UrlGithub, self.UrlGitee):
            try:
                # 本地项目不存在
                if os.path.exists(Constants.DirProjects):
                    # 如果文件夹存在则删除
                    AppLog.info('remove dir: {}'.format(Constants.DirProjects))
                    self.remove()
                AppLog.info('clone into dir: {}'.format(Constants.DirProjects))
                Signals.progressUpdated.emit(5, 100)
                self.clone(url)
                ok = True
                break
            except Exception as e:
                AppLog.error(str(e))
        if not ok:
            raise Exception('clone failed')

    def run(self):
        try:
            path = pygit2.discover_repository(Constants.DirProjects)
            if not path:
                self._clone()
            else:
                repo = pygit2.Repository(path)
                if repo.is_empty:  # 如果项目为空
                    self._clone()
                else:
                    # 重置并pull
                    AppLog.info('reset dir: {}'.format(Constants.DirProjects))
                    AppLog.info('reset target: {}'.format(repo.head.target))
                    repo.state_cleanup()
                    repo.reset(repo.head.target, pygit2.GIT_RESET_HARD)
                    Signals.progressUpdated.emit(5, 100)
                    AppLog.info('pull into dir: {}'.format(
                        Constants.DirProjects))
                    self.pull(repo)
                    Signals.progressStoped.emit()
        except Exception as e:
            AppLog.exception(e)

        AppLog.info('clone thread end')
        Signals.progressStoped.emit()
        Signals.cloneFinished.emit('')
        CloneThread.quit()


class UpgradeThread(QObject):
    """自动更新
    """

    UpdateUrl = [
        ('https://github.com/PyQt5/PyQtClient/raw/master/.Update/Upgrade.json',
         'https://github.com/PyQt5/PyQtClient/raw/master/.Update/Upgrade.{}.zip'
        ),
        ('https://gitee.com/PyQt5/PyQtClient/raw/master/.Update/Upgrade.json',
         'https://gitee.com/PyQt5/PyQtClient/raw/master/.Update/Upgrade.{}.zip'
        ),
        ('https://pyqt.site/PyQt5/PyQtClient/raw/master/.Update/Upgrade.json',
         'https://pyqt.site/PyQt5/PyQtClient/raw/master/.Update/Upgrade.{}.zip'
        ),
        ('https://pyqt5.com/PyQt5/PyQtClient/raw/master/.Update/Upgrade.json',
         'https://pyqt5.com/PyQt5/PyQtClient/raw/master/.Update/Upgrade.{}.zip')
    ]

    @classmethod
    def quit(cls):
        """退出线程
        :param cls:
        """
        if hasattr(cls, '_thread'):
            cls._thread.quit()
            AppLog.info('upgrade thread quit')

    @classmethod
    def start(cls, parent=None):
        """启动自动更新线程
        :param cls:
        """
        cls._thread = QThread(parent)
        cls._worker = UpgradeThread()
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('update thread started')

    def unzip(self, file):
        # 进行解压
        zipfile = ZipFile(file)
        path = os.path.abspath('.')
        members = zipfile.namelist()
        for zipinfo in members:
            _name = zipinfo.lower()
            if _name.endswith('.exe') or \
                    _name.endswith('.dll') or \
                    _name.endswith('.ttf') or \
                    _name.endswith('.so') or \
                    _name.endswith('.dylib'):
                tpath = os.path.abspath(os.path.join(path, zipinfo))
                # 需要重命名当前正在占用的文件
                if os.path.isfile(tpath):
                    os.rename(tpath, tpath + str(time()) + '.old')
            zipfile.extract(zipinfo, path)


#             zipfile.extractall(os.path.abspath('.'))
        zipfile.close()

    def download(self, file, url):
        AppLog.debug('start download {}'.format(url))
        with closing(requests.get(url, stream=True)) as response:
            # 单次请求最大值
            chunk_size = 1024
            # 内容体总大小
            content_size = int(response.headers['content-length'])
            data_count = 0
            Signals.updateProgressChanged.emit(0, 0, content_size)
            AppLog.debug('content_size: {}'.format(content_size))
            with open(file, 'wb') as fp:
                for data in response.iter_content(chunk_size=chunk_size):
                    fp.write(data)
                    data_count = data_count + len(data)
                    if content_size > 0:
                        Signals.updateProgressChanged.emit(
                            data_count, 0, content_size)
            # 解压
            self.unzip(file)
        AppLog.debug('download {} end'.format(file))

    def run(self):
        for url_ver, url_zip in self.UpdateUrl:
            try:
                show = True
                req = requests.get(url_ver)
                AppLog.info(req.text)
                if req.status_code != 200:
                    AppLog.info('update thread end')
                    UpgradeThread.quit()
                    return
                content = req.json()
                for version, text in content:
                    if Version.version < version:
                        if show:
                            Signals.updateDialogShowed.emit()
                            QThread.msleep(1000)
                        show = False
                        Signals.updateTextChanged.emit(str(Version.version),
                                                       str(version), text)
                        self.download(Constants.UpgradeFile.format(version),
                                      url_zip.format(version))
                Signals.updateFinished.emit(self.tr('update completed'))
                break
            except Exception as e:
                Signals.updateFinished.emit(
                    self.tr('update failed: {}').format(str(e)))
                AppLog.exception(e)

        AppLog.info('update thread end')
        UpgradeThread.quit()

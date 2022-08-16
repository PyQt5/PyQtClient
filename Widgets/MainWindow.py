#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Widgets.MainWindow
@description:
"""

import cgitb
import os
import sys
from random import randint

from PyQt5 import QtCore
from PyQt5.QtCore import (QCoreApplication, QEvent, QLibraryInfo, QProcess,
                          QProcessEnvironment, Qt, QTimer, QUrl, pyqtSlot)
from PyQt5.QtGui import QEnterEvent, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.uic import loadUi
from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils import Constants
from Utils.Application import QSingleApplication
from Utils.CommonUtil import AppLog, Setting, initLog
from Utils.GitThread import CloneThread, UpgradeThread

from Widgets.Dialogs.DonateDialog import DonateDialog
from Widgets.Dialogs.ErrorDialog import ErrorDialog
from Widgets.Dialogs.LoginDialog import LoginDialog
from Widgets.Dialogs.UpdateDialog import UpdateDialog
from Widgets.FramelessWindow import FramelessWindow
from Widgets.MainWindowBase import MainWindowBase


class MainWindow(FramelessWindow, MainWindowBase, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        Setting.init(self)
        self._initLanguage()
        self._initUi()
        self._initSignals()
        # 加载窗口大小并恢复
        geometry = Setting.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        # 200毫秒后显示登录对话框
        QTimer.singleShot(200, self._initCatalog)
        QTimer.singleShot(500, self.treeViewCatalogs.initCatalog)
        # 初始化网页
        QTimer.singleShot(500, self._initWebView)
        # 检测更新
        QTimer.singleShot(5000, UpgradeThread.start)
        # 显示捐赠窗口
        QTimer.singleShot(randint(1000 * 60 * 5, 2000 * 60 * 5),
                          self._initDonate)

    def initLogin(self):
        dialog = LoginDialog(self)
        dialog.exec_()
        # 刷新头像样式
        if Constants._Account != '' and Constants._Password != '':
            self.buttonHead.image = Constants.ImageAvatar
            self.buttonHead.setToolTip(Constants._Username)

    def _initDonate(self):
        # 显示捐赠窗口
        alipayImg = os.path.join(Constants.DirProjects, 'Donate',
                                 'zhifubao.png')
        wechatImg = os.path.join(Constants.DirProjects, 'Donate', 'weixin.png')
        if os.path.exists(alipayImg) and os.path.exists(wechatImg):
            dialog = DonateDialog(alipayImg, wechatImg, self)
            dialog.exec_()

    def _initUpdate(self):
        # 显示更新对话框
        self.udialog = UpdateDialog()
        self.udialog.show()

    def _initCatalog(self):
        # 更新目录
        self._showNotice(
            QCoreApplication.translate('MainWindow', 'Update Example Started'))
        CloneThread.start()

    @pyqtSlot(str)
    def renderCode(self, code):
        """显示代码
        """
        content = repr(code)
        self._runJs("updateCode({});".format(content))

    @pyqtSlot(str)
    def renderReadme(self, path=''):
        """加载README.md并显示
        """
        path = path.replace('\\', '/')
        if not path:
            path = os.path.join(Constants.DirProjects, 'README.md')
            Constants.CurrentReadme = ''
        elif path.count('/') == 0:
            path = os.path.join(Constants.DirCurrent, path, 'README.md')
            Constants.CurrentReadme = path
        elif not path.endswith('README.md'):
            path = path + '/README.md'
            Constants.CurrentReadme = path
        if not os.path.exists(path):
            AppLog.debug('{} not exists'.format(path))
            self._runJs('updateText("");')
            return
        if not os.path.isfile(path):
            AppLog.warn('file {} not exists'.format(path))
            return
        Constants.DirCurrent = os.path.dirname(path).replace('\\', '/')
        AppLog.debug('DirCurrent change to: {}'.format(Constants.DirCurrent))
        AppLog.debug('render: {}'.format(path))
        Constants.CurrentReadme = path  # 记录打开的路径防止重复加载
        AppLog.debug('readme dir: {}'.format(Constants.DirCurrent))
        content = repr(open(path, 'rb').read().decode())
        self._runJs("updateText({});".format(content))

    def _exposeInterface(self):
        """向Js暴露调用本地方法接口
        """
        self.webViewContent.page().mainFrame().addToJavaScriptWindowObject(
            '_mainWindow', self)

    def _runFile(self, file):
        """子进程运行文件
        :param file:    文件
        """
        file = os.path.abspath(file)
        process = QProcess(self)
        process.setProperty('file', file)
        process.readChannelFinished.connect(self.onReadChannelFinished)

        env = QProcessEnvironment.systemEnvironment()
        #         libpath = get_python_lib()
        #         env.insert('QT_QPA_PLATFORM_PLUGIN_PATH', os.path.join(
        #             libpath, 'PyQt5', 'Qt', 'plugins', 'platforms'))
        #         env.insert('QT_QPA_PLATFORM_PLUGIN_PATH',
        #                    os.path.abspath('platforms'))
        env.insert('QML_IMPORT_PATH', os.path.abspath('qml'))
        env.insert('QML2_IMPORT_PATH', env.value('QML_IMPORT_PATH'))
        if os.name == 'nt':
            env.insert(
                'PATH',
                QLibraryInfo.location(QLibraryInfo.BinariesPath) + os.pathsep +
                env.value('PATH'))
        env.insert(
            'PATH',
            os.path.dirname(os.path.abspath(sys.argv[0])) + os.pathsep +
            env.value('PATH'))
        process.setProcessEnvironment(env)

        #         if sys.executable.endswith('python.exe'):
        process.setWorkingDirectory(os.path.dirname(file))
        process.start(sys.executable, [file])

    def _runUiFile(self, file):
        """预览UI文件
        :param file:    文件
        """
        try:
            dialog = QDialog(self)
            layout = QVBoxLayout(dialog)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(loadUi(file))
            dialog.exec_()
        except Exception as e:
            AppLog.warn('run ui file failed: {}'.format(str(e)))

    def _runJs(self, code):
        """执行js
        :param code:
        """
        self.webViewContent.page().mainFrame().evaluateJavaScript(code)

    def onReadChannelFinished(self):
        process = self.sender()
        message = process.readAllStandardError().data()
        try:
            message = message.decode(errors='ignore')
        except Exception as e:
            AppLog.exception(e)
            return
        if process.exitCode() != 0 and len(message.strip()) > 0:
            file = str(process.property('file'))
            reqfile = os.path.abspath(
                os.path.join(os.path.dirname(file), 'requirements.txt'))
            AppLog.debug('reqfile: {}'.format(reqfile))
            dialog = ErrorDialog(message, self, reqfile=reqfile)
            dialog.exec_()

    def onUrlLoaded(self, name):
        """加载带参数网址
        :param name:
        """
        url = QUrl.fromLocalFile(os.path.abspath(Constants.HomeFile))
        url.setQuery('name={}'.format(name))
        self.webViewContent.load(url)

    def onAnchorJumped(self, word):
        """锚点跳转
        :param word:
        """
        if not word:
            return
        self._runJs('$("h2:contains({})")[0].scrollIntoView();'.format(word))

    def onLinkClicked(self, url):
        """加载网址
        :param url:
        """
        self.webViewContent.load(QUrl(url))

    def closeEvent(self, event):
        # 储存窗口位置
        Setting.setValue('geometry', self.saveGeometry())
        super(MainWindow, self).closeEvent(event)

    def eventFilter(self, obj, event):
        # 事件过滤器
        if obj == self.widgetMain and isinstance(event, QEnterEvent):
            # 用于解决鼠标进入其它控件后还原为标准鼠标样式
            self.setCursor(Qt.ArrowCursor)
        return FramelessWindow.eventFilter(self, obj, event)

    def changeEvent(self, event):
        # 窗口改变事件
        FramelessWindow.changeEvent(self, event)
        if event.type() == QEvent.WindowStateChange:  # 窗口状态改变
            state = self.windowState()
            if state == (state | Qt.WindowMaximized):
                # 最大化状态,显示还原按钮
                self.buttonMaximum.setVisible(False)
                self.buttonNormal.setVisible(True)
            else:
                # 隐藏还原按钮
                self.buttonMaximum.setVisible(True)
                self.buttonNormal.setVisible(False)


def main():
    if int(QtCore.PYQT_VERSION_STR.split('.')[1]) > 5:
        # for > Qt 5.5
        os.putenv('QT_AUTO_SCREEN_SCALE_FACTOR', '1')
    else:
        # for Qt 5.5
        os.putenv('QT_DEVICE_PIXEL_RATIO', 'auto')
    if os.name == 'nt':
        os.environ['PATH'] = QLibraryInfo.location(
            QLibraryInfo.BinariesPath) + os.pathsep + os.environ['PATH']
    os.makedirs(Constants.DirErrors, exist_ok=True)
    os.makedirs(Constants.DirProject, exist_ok=True)
    os.makedirs(os.path.dirname(Constants.UpgradeFile), exist_ok=True)
    # 异常捕捉
    sys.excepthook = cgitb.Hook(1, Constants.DirErrors, 5, sys.stderr, '')
    # 初始化日志
    initLog(Constants.LogName, Constants.LogFile)
    # 运行app
    app = QSingleApplication('qtsingleapp-pyqtclient', sys.argv)
    if app.isRunning():
        # 激活窗口
        app.sendMessage('show', 1000)
    else:
        app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        app.setQuitOnLastWindowClosed(True)
        app.setWindowIcon(QIcon('Resources/Images/app.ico'))
        # 第一次运行
        w = MainWindow()
        app.setActivationWindow(w)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir('../')
    main()

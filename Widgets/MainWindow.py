#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.MainWindow
@description:
"""
import cgitb
from multiprocessing import Process
import os
import sys

from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSlot, QUrl
from PyQt5.QtGui import QEnterEvent

from Dialogs.LoginDialog import LoginDialog
from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils import Constants
from Utils.Application import QSingleApplication
from Utils.CommonUtil import initLog, AppLog, Setting
from Utils.GitThread import CloneThread
from Widgets.FramelessWindow import FramelessWindow
from Widgets.MainWindowBase import MainWindowBase


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


def runCode(file):
    from Utils import RunCode
    RunCode.runCode(file)


class MainWindow(FramelessWindow, MainWindowBase, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        Setting.init(self)
        self._initUi()
        self._initSignals()
        # 加载窗口大小并恢复
        geometry = Setting.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        # 200毫秒后显示登录对话框
        QTimer.singleShot(200, self._initCatalog)
        # 初始化网页
        QTimer.singleShot(500, self._initWebView)

    def initLogin(self):
        dialog = LoginDialog(self)
        dialog.exec_()
        # 刷新头像样式
        if Constants._Account != '' and Constants._Password != '':
            self.buttonHead.image = Constants.ImageAvatar
            self.buttonHead.setToolTip(Constants._Username)
    
    def _initCatalog(self):
        # 更新目录
        CloneThread.start(self)

    @pyqtSlot()
    def renderReadme(self, path=None):
        """加载README.md并显示
        """
        if not path:
            path = os.path.join(Constants.DirProjects, 'README.md')
        if not os.path.exists(path):
            self._runJs('updateText("");')
            return
        if not os.path.isfile(path):
            AppLog.warn('file {} not exists'.format(path))
            return
        Constants.DirCurrent = os.path.dirname(path).replace('\\', '/')
        if Constants.CurrentReadme == path:
            return
        Constants.CurrentReadme = path      # 记录打开的路径防止重复加载
        AppLog.debug('render: {}'.format(path))
        AppLog.debug('readme dir: {}'.format(Constants.DirCurrent))
        content = repr(open(path, 'rb').read().decode())
        self._runJs("updateText({});".format(content))

    def _exposeInterface(self):
        """向Js暴露调用本地方法接口
        """
        self.webViewContent.page().mainFrame().addToJavaScriptWindowObject('_mainWindow', self)

    def _runFile(self, file):
        """子进程运行文件
        :param file:    文件
        """
        p = Process(target=runCode, args=(os.path.abspath(file),))
        p.start()

    def _runJs(self, code):
        """执行js
        :param code:
        """
        self.webViewContent.page().mainFrame().evaluateJavaScript(code)

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
    # for Qt 5.5
    os.putenv('QT_DEVICE_PIXEL_RATIO', 'auto')
    # for > Qt 5.5
    os.putenv('QT_AUTO_SCREEN_SCALE_FACTOR', '1')
    os.makedirs(Constants.DirErrors, exist_ok=True)
    os.makedirs(Constants.DirProject, exist_ok=True)
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
        app.setQuitOnLastWindowClosed(True)
        # 第一次运行
        w = MainWindow()
        app.setActivationWindow(w)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir('../')
    main()

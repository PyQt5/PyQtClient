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
import os
import sys

from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QStandardItem, QEnterEvent

from Dialogs.LoginDialog import LoginDialog
from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils import Constants
from Utils.Application import QSingleApplication
from Utils.CommonUtil import initLog, AppLog, Setting
from Utils.Repository import DirRunnable
from Widgets.FramelessWindow import FramelessWindow
from Widgets.MainWindowBase import MainWindowBase


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class MainWindow(FramelessWindow, MainWindowBase, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        Setting.init(self)
        self._initUi()
        self._initThread()
        self._initSignals()
        # 加载窗口大小并恢复
        geometry = Setting.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        # 200毫秒后显示登录对话框
        QTimer.singleShot(200, self.initLogin)
        # 初始化网页
        QTimer.singleShot(500, self._initWebView)

    def onRunnableFinished(self, path):
        """任务运行完毕后删除该path
        :param path:
        """
        AppLog.debug('finished get path: {}'.format(path))
        if path in self._runnables:
            self._runnables.remove(path)

    def onItemAdded(self, names, rpath):
        """线程发送信号增加Item
        :param names:
        :param rpath:
        """
        AppLog.debug('names: {}'.format(str(names)))
        file = ''  # 路径
        pItem = None  # 上级item
        if len(names) == 1 and 'Donate' in names:
            return
        for name in names:
            items = self._dmodel.findItems(name)
            if not items:
                # 如果没有找到上级Item则新增加一个
                item = QStandardItem(self._dmodel.invisibleRootItem())
                item.setText(name)
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(name, Constants.RoleName)
                file = os.path.join(file, name)
                item.setData(file.replace('\\', '/'), Constants.RolePath)
                file = os.path.join(Constants.DirProjects, file)
                item.setData(file.replace('\\', '/'), Constants.RoleFile)
                if pItem:
                    pItem.appendRow(item)
                else:
                    self._dmodel.appendRow(item)
                pItem = item
            else:
                for item in items:
                    if item.data(Constants.RoleFile) == rpath:
                        pItem = item
                        break

    def initLogin(self):
        dialog = LoginDialog(self)
        dialog.exec_()
        # 刷新头像样式
        if Constants._Account != None and Constants._Password != None:
            self.buttonHead.image = Constants.ImageAvatar
            self.buttonHead.setToolTip(Constants._Username)
            # 更新根目录
            if '/' not in self._runnables:
                self._runnables.add('/')
                self._threadPool.start(DirRunnable(
                    '', Constants._Account, Constants._Password))

    @pyqtSlot()
    def renderReadme(self, path=None):
        """加载README.md并显示
        """
        if not path:
            path = os.path.join(Constants.DirProjects, 'README.md')
        if not os.path.exists(path):
            self._runJs('updateText("");')
            return
        Constants.DirCurrent = os.path.dirname(path).replace('\\', '/')
        Constants.CurrentReadme = path      # 记录打开的路径防止重复加载
        AppLog.debug('render: {}'.format(path))
        AppLog.debug('readme dir: {}'.format(Constants.DirCurrent))
        content = repr(open(path, 'rb').read().decode())
        self._runJs("updateText({});".format(content))

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
    os.putenv('QT_DEVICE_PIXEL_RATIO', 'auto')
    os.makedirs(Constants.DirErrors, exist_ok=True)
    os.makedirs(Constants.DirProjects, exist_ok=True)
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

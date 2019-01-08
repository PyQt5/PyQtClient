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
from pathlib import Path
import sys
import webbrowser

from PyQt5.QtCore import QEvent, Qt, pyqtSlot, QTimer, QThreadPool,\
    QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils import Constants
from Utils.Application import QSingleApplication
from Utils.CommonUtil import initLog, AppLog, Signals
from Utils.Constants import LogName, DirErrors, DirProjects, LogFile, UrlProject, \
    UrlQQ, UrlGroup
from Utils.Repository import RootRunnable
from Utils.ThemeManager import ThemeManager
from Widgets.FramelessWindow import FramelessWindow
from Widgets.LoginDialog import LoginDialog
from Widgets.ToolTip import ToolTip


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class MainWindow(FramelessWindow, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 绑定返回顶部提示框
        ToolTip.bind(self.buttonBacktoUp)
        # 隐藏进度条
        self.progressBar.setVisible(False)
        # 隐藏还原按钮
        self.buttonNormal.setVisible(False)
        # 安装事件过滤器用于还原鼠标样式
        self.widgetMain.installEventFilter(self)
        # 加载主题
        ThemeManager.loadTheme(self)
        # 加载鼠标样式
        ThemeManager.loadCursor(self.widgetMain)
        # 设置目录树Model
        self._dmodel = QStandardItemModel(self.treeViewCatalogs)
        self._fmodel = QSortFilterProxyModel(self.treeViewCatalogs)
        self._fmodel.setSourceModel(self._dmodel)
        self.treeViewCatalogs.setModel(self._fmodel)
        # 200毫秒后显示登录对话框
        QTimer.singleShot(200, self.initLogin)
        # 创建线程池,最多5个线程
        self._threadPool = QThreadPool(self)
        self._threadPool.setMaxThreadCount(5)
        # 绑定全局信号槽
        Signals.progressBarShowed.connect(
            self.showProgressBar, type=Qt.QueuedConnection)
        Signals.itemAdded.connect(self.onItemAdded, type=Qt.QueuedConnection)

    def closeEvent(self, event):
        if hasattr(self, '_repoThread'):
            self._repoThread.stoped = True
        super(MainWindow, self).closeEvent(event)

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

    def showProgressBar(self, visible=True):
        """显示或隐藏进度条
        """
        self.progressBar.setVisible(visible)

    def onItemAdded(self, names):
        AppLog.debug('names: {}'.format(str(names)))

    def initLogin(self):
        dialog = LoginDialog(self)
        dialog.exec_()
        # 刷新头像样式
        if Constants._Github != None:
            self.style().polish(self.buttonHead)
        # 遍历本地缓存目录
        self.initCatalog()

    def initCatalog(self):
        """初始化本地仓库结构树
        """
        if self._dmodel.rowCount() == 0:
            for path in Path(DirProjects).rglob('*'):
                if path.is_file():  # 跳过文件
                    continue
                if path.name.startswith('.'):  # 不显示.开头的文件夹
                    continue
                item = QStandardItem(path.name)
                item.setData(path)
                self._dmodel.appendRow(item)
        if Constants._Github != None:
            # 更新根目录
            self._threadPool.start(RootRunnable())

    @pyqtSlot()
    def on_buttonSkin_clicked(self):
        """选择主题样式
        """
        pass

    @pyqtSlot()
    def on_buttonMinimum_clicked(self):
        """最小化
        """
        self.showMinimized()

    @pyqtSlot()
    def on_buttonMaximum_clicked(self):
        """最大化
        """
        self.showMaximized()

    @pyqtSlot()
    def on_buttonNormal_clicked(self):
        """还原
        """
        self.showNormal()

    @pyqtSlot()
    def on_buttonClose_clicked(self):
        """关闭
        """
        self.close()

    @pyqtSlot()
    def on_buttonHead_clicked(self):
        """点击头像
        """
        if Constants._Github == None:
            self.initLogin()

    @pyqtSlot()
    def on_buttonSearch_clicked(self):
        """点击搜索按钮
        """
        pass

    @pyqtSlot()
    def on_buttonGithub_clicked(self):
        """点击项目按钮
        """
        webbrowser.open_new_tab(UrlProject)

    @pyqtSlot()
    def on_buttonQQ_clicked(self):
        """点击QQ按钮
        """
        webbrowser.open(UrlQQ)

    @pyqtSlot()
    def on_buttonGroup_clicked(self):
        """点击群按钮
        """
        webbrowser.open(UrlGroup)

    @pyqtSlot()
    def on_buttonBackup_clicked(self):
        """点击返回按钮
        """
        pass


def main():
    os.putenv('QT_DEVICE_PIXEL_RATIO', 'auto')
    os.makedirs(DirErrors, exist_ok=True)
    os.makedirs(DirProjects, exist_ok=True)
    # 异常捕捉
    sys.excepthook = cgitb.Hook(1, DirErrors, 5, sys.stderr, '')
    # 初始化日志
    initLog(LogName, LogFile)
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

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

from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import QStandardItem, QEnterEvent

from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils import Constants
from Utils.Application import QSingleApplication
from Utils.CommonUtil import initLog, AppLog, Setting
from Utils.Repository import DirRunnable
from Widgets.FramelessWindow import FramelessWindow
from Widgets.LoginDialog import LoginDialog
from Widgets.MainWindowBase import MainWindowBase


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class MainWindow(FramelessWindow, MainWindowBase, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self._initUi()
        self._initModel()
        self._initThread()
        self._initSignals()
        # 加载窗口大小并恢复
        geometry = Setting.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        # 200毫秒后显示登录对话框
        QTimer.singleShot(200, self.initLogin)

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
        # 遍历本地缓存目录
        self.initCatalog()
        dialog = LoginDialog(self)
        dialog.exec_()
        # 刷新头像样式
        if Constants._Github != None:
            self.buttonHead.image = Constants.ImageAvatar
#             self.style().polish(self.buttonHead)
            # 更新根目录
            self._threadPool.start(DirRunnable(''))

    def initCatalog(self):
        """初始化本地仓库结构树
        """
        if self._dmodel.rowCount() == 0:
            pitem = self._dmodel.invisibleRootItem()
            # 只遍历根目录
            for name in os.listdir(Constants.DirProjects):
                file = os.path.join(Constants.DirProjects,
                                    name).replace('\\', '/')
                if os.path.isfile(file):  # 跳过文件
                    continue
                if name.startswith('.') or name == 'Donate' or name == 'Test':  # 不显示.开头的文件夹
                    continue
                item = QStandardItem(pitem)
                item.setText(name)
                # 添加自定义的数据
                item.setData(name, Constants.RoleName)        # 文件夹名字
                item.setData(file, Constants.RoleFile)        # 本地文件夹路径
                item.setData(name, Constants.RolePath)        # 用于请求远程的路径
                pitem.appendRow(item)
            # 排序
            self._fmodel.sort(0, Qt.AscendingOrder)
            # 初始化网页
            QTimer.singleShot(500, self._initWebView)

    def on_treeViewCatalogs_clicked(self, modelIndex):
        """被点击的item
        :param modelIndex:        代理模型中的QModelIndex, 并不是真实的
        """
        path = modelIndex.data(Constants.RolePath)
        if path not in self._runnables:
            AppLog.debug('path: {}'.format(path))
            AppLog.debug('name: {}'.format(
                modelIndex.data(Constants.RoleName)))
            rdir = modelIndex.data(Constants.RoleFile)
            AppLog.debug('file: {}'.format(rdir))
            self.renderReadme(path=os.path.join(rdir, 'README.md'))
            if Constants._Github != None:
                self._runnables.add(path)
                self._threadPool.start(DirRunnable(path))

    def renderReadme(self, *, path=None):
        """加载README.md并显示
        """
        try:
            self.webViewContent.loadFinished.disconnect(self.renderReadme)
        except:
            pass
        if path == None:
            path = os.path.join(Constants.DirProjects, 'README.md')
        if not os.path.exists(path):
            return
        Constants.DirCurrent = os.path.dirname(path).replace('\\', '/')
        AppLog.debug('render: {}'.format(path))
        AppLog.debug('readme dir: {}'.format(Constants.DirCurrent))
        content = repr(open(path, 'rb').read().decode())
        self._runJs("updateText({});".format(content))

    def closeEvent(self, event):
        # 储存窗口位置
        Setting.setValue('geometry', self.saveGeometry())
        if hasattr(self, '_repoThread'):
            self._repoThread.stoped = True
        super(MainWindow, self).closeEvent(event)

    def eventFilter(self, obj, event):
        # 事件过滤器
        if obj == self.widgetMain and isinstance(event, QEnterEvent):
            # 用于解决鼠标进入其它控件后还原为标准鼠标样式
            self.setCursor(Qt.ArrowCursor)
        elif obj == self.treeViewCatalogs:
            types = event.type()
            if types == QEvent.Enter:
                # 鼠标进入显示滚动条
                self.treeViewCatalogs.verticalScrollBar().setVisible(True)
            elif types == QEvent.Leave:
                # 鼠标离开隐藏滚动条
                self.treeViewCatalogs.verticalScrollBar().setVisible(False)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月13日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.TreeView
@description: 
"""
import os

from PyQt5.QtCore import pyqtProperty, Qt
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView

from Utils import Constants
from Utils.CommonUtil import AppLog, Signals
from Utils.SortFilterModel import SortFilterModel
from Utils.StyledItemDelegate import StyledItemDelegate


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class TreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super(TreeView, self).__init__(*args, **kwargs)
        # 进度条背景颜色
        self._barColor = QColor(255, 255, 255)
        self._initModel()
        self._initSignals()
        # 设置自定义委托代理用于绘制下载进度
        self.setItemDelegate(StyledItemDelegate(self))
        self.initCatalog()

    def _initModel(self):
        """设置目录树Model"""
        self._dmodel = QStandardItemModel(self)
        self._fmodel = SortFilterModel(self)
        self._fmodel.setSourceModel(self._dmodel)
        self.setModel(self._fmodel)
    
    def _initSignals(self):
        Signals.filterChanged.connect(self._fmodel.setFilterRegExp)
        self.doubleClicked.connect(self.onDoubleClicked)

    def listSubDir(self, pitem, path):
        """遍历子目录
        :param item:    上级Item
        :param path:    目录
        """
        paths = os.listdir(path)
        files = []
        for name in paths:
            spath = os.path.join(path, name)
            if not os.path.isfile(spath):
                continue
            spath = os.path.splitext(spath)
            if len(spath) == 0:
                continue
            if spath[1] == '.py' and spath[0].endswith('__init__') == False:
                files.append(name)

        if pitem.rowCount() != 0 and len(files) == pitem.rowCount():
            return
        for name in files:
            file = os.path.join(path, name).replace('\\', '/')
            item = QStandardItem(pitem)
            item.setText(name)
            # 添加自定义的数据
            item.setData(False, Constants.RoleRoot)       # 不是根目录
            item.setData(name, Constants.RoleName)        # 文件名字
            item.setData(file, Constants.RoleFile)        # 本地文件路径
            item.setData(None, Constants.RolePath)
            pitem.appendRow(item)

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
                item.setData(True, Constants.RoleRoot)        # 根目录
                item.setData(name, Constants.RoleName)        # 文件夹名字
                item.setData(file, Constants.RoleFile)        # 本地文件夹路径
                item.setData(name, Constants.RolePath)        # 用于请求远程的路径
                item.setData(0, Constants.RoleValue)          # 当前进度
                item.setData(0, Constants.RoleTotal)          # 总进度
                pitem.appendRow(item)
                # 遍历子目录
                self.listSubDir(item, file)
            # 排序
            self._fmodel.sort(0, Qt.AscendingOrder)

    def onDoubleClicked(self, modelIndex):
        """Item双击
        :param modelIndex:        此处是代理模型中的QModelIndex, 并不是真实的
        """
        path = modelIndex.data(Constants.RolePath)
        rdir = modelIndex.data(Constants.RoleFile)
        AppLog.debug('path: {}'.format(path))
        AppLog.debug('name: {}'.format(
            modelIndex.data(Constants.RoleName)))
        AppLog.debug('dir or file: {}'.format(rdir))
        # 是否需要遍历本地子目录并显示
        item = self._dmodel.itemFromIndex(self._fmodel.mapToSource(modelIndex))
        if os.path.isfile(rdir):
            # 运行代码
            self._runFile(rdir)
        elif item and path:
            # 是否需要加载README.md
#             self.renderReadme(path=os.path.join(rdir, 'README.md'))
            self.listSubDir(item, rdir)
        if item.rowCount() == 0:
            # 尝试后台获取远程目录数据
            if Constants._Account != None and Constants._Password != None:
                if path not in self._runnables:
                    self._runnables.add(path)
#                     self._threadPool.start(DirRunnable(item, path,Constants._Account))

    def enterEvent(self, event):
        super(TreeView, self).enterEvent(event)
        # 鼠标进入显示滚动条
        self.verticalScrollBar().setVisible(True)

    def leaveEvent(self, event):
        super(TreeView, self).leaveEvent(event)
        # 鼠标离开隐藏滚动条
        self.verticalScrollBar().setVisible(False)

    @pyqtProperty(QColor)
    def barColor(self):
        return self._barColor

    @barColor.setter
    def barColor(self, color):
        self._barColor = QColor(color)
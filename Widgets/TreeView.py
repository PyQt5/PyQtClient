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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView

from Utils import Constants
from Utils.CommonUtil import AppLog, Signals
from Utils.SortFilterModel import SortFilterModel


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class TreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super(TreeView, self).__init__(*args, **kwargs)
        self._initModel()
        self._initSignals()
        self.initCatalog()

    def _initModel(self):
        """设置目录树Model"""
        self._dmodel = QStandardItemModel(self)
        self._fmodel = SortFilterModel(self)
        self._fmodel.setSourceModel(self._dmodel)
        self.setModel(self._fmodel)

    def _initSignals(self):
        Signals.itemJumped.connect(self.onItemJumped)
        Signals.filterChanged.connect(self._fmodel.setFilterRegExp)
        self.doubleClicked.connect(self.onDoubleClicked)

    def rootItem(self):
        """得到根节点Item"""
        return self._dmodel.invisibleRootItem()

    def findItems(self, name):
        """根据名字查找item
        :param name:
        """
        return self._dmodel.findItems(name)

    def onItemJumped(self, name):
        items = self.findItems(name)
        if not items:
            return
        index = self._fmodel.mapFromSource(
            self._dmodel.indexFromItem(items[0]))
        self.setCurrentIndex(index)
        self.expand(index)
#         # 显示readme
#         Signals.showReadmed.emit(os.path.join(
#             Constants.DirProjects, name, 'README.md'))

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

        # 已经存在的item
        existsItems = [pitem.child(i).text() for i in range(pitem.rowCount())]

        for name in files:
            if name in existsItems:
                continue
            file = os.path.join(path, name).replace('\\', '/')
            item = QStandardItem(name)
            # 添加自定义的数据
            item.setData(False, Constants.RoleRoot)       # 不是根目录
            item.setData(file, Constants.RolePath)
            pitem.appendRow(item)

    def initCatalog(self):
        """初始化本地仓库结构树
        """
        AppLog.debug('')
        if not os.path.exists(Constants.DirProjects):
            return
        pitem = self._dmodel.invisibleRootItem()
        # 只遍历根目录
        for name in os.listdir(Constants.DirProjects):
            file = os.path.join(Constants.DirProjects,
                                name).replace('\\', '/')
            if os.path.isfile(file):  # 跳过文件
                continue
            if name.startswith('.') or name == 'Donate' or name == 'Test':  # 不显示.开头的文件夹
                continue
            items = self.findItems(name)
            if items:
                item = items[0]
            else:
                item = QStandardItem(name)
                # 添加自定义的数据
                # 用于绘制进度条的item标识
                item.setData(True, Constants.RoleRoot)
                # 目录或者文件的绝对路径
                item.setData(os.path.abspath(os.path.join(
                    Constants.DirProjects, name)), Constants.RolePath)
                pitem.appendRow(item)
            # 遍历子目录
            self.listSubDir(item, file)
        # 排序
        self._fmodel.sort(0, Qt.AscendingOrder)

    def onDoubleClicked(self, modelIndex):
        """Item双击
        :param modelIndex:        此处是代理模型中的QModelIndex, 并不是真实的
        """
        root = modelIndex.data(Constants.RoleRoot)
        path = modelIndex.data(Constants.RolePath)
        AppLog.debug('is root: {}'.format(root))
        AppLog.debug('path: {}'.format(path))
        if not root and os.path.isfile(path):
            # 运行代码
            Signals.runExampled.emit(path)
        if root and os.path.isdir(path):
            # 显示readme
            Signals.showReadmed.emit(os.path.join(path, 'README.md'))

    def enterEvent(self, event):
        super(TreeView, self).enterEvent(event)
        # 鼠标进入显示滚动条
        self.verticalScrollBar().setVisible(True)

    def leaveEvent(self, event):
        super(TreeView, self).leaveEvent(event)
        # 鼠标离开隐藏滚动条
        self.verticalScrollBar().setVisible(False)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestTreeView
@description: 
"""
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTreeView, QTreeWidget,\
    QTreeWidgetItem

from Utils import Constants
from Widgets.TreeView import TreeView


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class MyTreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super(MyTreeView, self).__init__(*args, **kwargs)
        self._initModel()
        self.initCatalog()

    def _initModel(self):
        """设置目录树Model"""
        self._dmodel = QStandardItemModel(self)
        self._fmodel = QSortFilterProxyModel(self)
        self._fmodel.setSourceModel(self._dmodel)
        self.setModel(self._fmodel)
        pitem = self._dmodel.invisibleRootItem()
        pitem.appendRow(QStandardItem('root'))

    def initCatalog(self):
        """初始化本地仓库结构树
        """
        pitem = self._dmodel.invisibleRootItem()
        # 只遍历根目录
        for name in os.listdir(Constants.DirProjects):
            file = os.path.join(Constants.DirProjects,
                                name).replace('\\', '/')
            if os.path.isfile(file):  # 跳过文件
                continue
            if name.startswith('.') or name == 'Donate' or name == 'Test':  # 不显示.开头的文件夹
                continue
            item = QStandardItem(name)
            # 添加自定义的数据
            item.setData(True, Constants.RoleRoot)        # 根目录
            item.setData(name, Constants.RoleName)        # 文件夹名字
            item.setData(file, Constants.RoleFile)        # 本地文件夹路径
            item.setData(name, Constants.RolePath)        # 用于请求远程的路径
            item.setData(0, Constants.RoleValue)          # 当前进度
            item.setData(0, Constants.RoleTotal)          # 总进度
            pitem.appendRow(item)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        layout = QHBoxLayout(self)

        t1 = TreeView(self, objectName='treeViewCatalogs')
        layout.addWidget(t1)

        t2 = QTreeView(self)
        model = QStandardItemModel(t2)
        fmodel = QSortFilterProxyModel(t2)
        fmodel.setSourceModel(model)
        t2.setModel(fmodel)
        pitem = model.invisibleRootItem()
        pitem.appendRow(QStandardItem('root'))
        layout.addWidget(t2)

        t4 = MyTreeView(self)
        layout.addWidget(t4)

        t3 = QTreeWidget(self)
        layout.addWidget(t3)
        ritem = QTreeWidgetItem(t3)
        ritem.setText(0, 'root')
        t3.addTopLevelItem(ritem)


if __name__ == '__main__':
    import sys
    import os
    os.chdir('../')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet("""/*目录树*/
QTreeView {
    outline: none;  /*去掉虚线框*/
    border: none;       /*无边框*/
    color: rgba(255, 255, 255, 200);
    background-color: transparent;    /*背景透明*/
    /*item 进度条颜色*/
    qproperty-barColor: rgb(255, 255, 255);
}

QTreeView::item {
    min-height: 36px;
}

QTreeView::item:hover {
    color: rgba(255, 255, 255, 255);
    background: red;
}

QTreeView::item:selected {
    color: rgba(255, 255, 255, 255);
    background: yellow;
}

QTreeView::item:selected:active{
    color: rgba(255, 255, 255, 255);
    background: blue;
}

QTreeView::item:selected:!active {
    color: rgba(255, 255, 255, 200);
    background: green;
}
    """)
    w = Window()
    w.show()
    sys.exit(app.exec_())

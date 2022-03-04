#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月15日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestTreeView
@description: 
"""

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QHBoxLayout, QTreeView, QTreeWidget,
                             QTreeWidgetItem, QWidget)
from Widgets.TreeView import TreeView

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


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

        t3 = QTreeWidget(self)
        layout.addWidget(t3)
        ritem = QTreeWidgetItem(t3)
        ritem.setText(0, 'root')
        t3.addTopLevelItem(ritem)


if __name__ == '__main__':
    import cgitb
    import os
    import sys
    os.chdir('../')
    sys.excepthook = cgitb.enable(1, None, 5, '')
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

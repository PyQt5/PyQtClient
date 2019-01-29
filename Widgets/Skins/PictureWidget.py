#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月29日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.PictureWidget
@description: 
"""
from PyQt5.QtCore import QThreadPool

from Utils.CommonUtil import Signals
from Utils.ThemeThread import GetAllCategoryRunnable
from Widgets.Skins.SkinBaseWidget import SkinBaseWidget, SkinBaseItemWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class PictureItemWidget(SkinBaseItemWidget):

    pass


class PictureWidget(SkinBaseWidget):

    def __init__(self, cid, *args, **kwargs):
        super(PictureWidget, self).__init__(*args, **kwargs)
        self.cid = cid
        self.items = []

    def setItems(self, items):
        self.items = items

    def addItem(self, index, path):
        # 计算行列
        return
        self.gridLayout.addWidget(
            SkinBaseItemWidget('', path, Signals.pictureItemClicked, self), row, col)

    def init(self):
        """初始化该分类
        """
        if self.gridLayout.count() > 0:
            return
        QThreadPool.start(GetAllCategoryRunnable(self.cid, self))

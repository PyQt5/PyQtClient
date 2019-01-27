#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.ThemeWidget
@description: 
"""
from Utils.CommonUtil import Signals
from Utils.ThemeThread import ThemeThread
from Widgets.Skins.SkinBaseWidget import PixmapWidth, PixmapHeight,\
    SkinBaseItemWidget, SkinBaseWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ThemeWidget(SkinBaseWidget):

    def __init__(self, *args, **kwargs):
        super(ThemeWidget, self).__init__(*args, **kwargs)
        Signals.themeItemAdded.connect(self.onThemeItemAdded)
        Signals.themeItemAddFinished.connect(
            self.onThemeItemAddFinished)

    def init(self):
        """初始化主题
        """
        if self.gridLayout.count() > 0:
            return
        ThemeThread.start(PixmapWidth, PixmapHeight)

    def onThemeItemAddFinished(self):
        """添加完成
        """
        return

    def onThemeItemAdded(self, row, col, name, path):
        """
        :param row:            行
        :param col:            列
        :param name:           名字
        :param path:           路径
        """
        self.lastRow = row
        self.lastCol = col
        self.gridLayout.addWidget(
            SkinBaseItemWidget(name, path, Signals.colourfulItemClicked, self), row, col)

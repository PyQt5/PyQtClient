#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.ColourfulWidget
@description: 多彩控件
"""

from PyQt5.QtWidgets import QPushButton

from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager
from Utils.ThemeThread import ColourfulThread
from Widgets.Skins.SkinBaseWidget import SkinBaseWidget, SkinBaseItemWidget,\
    PixmapWidth, PixmapHeight


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ColourfulWidget(SkinBaseWidget):

    def __init__(self, *args, **kwargs):
        super(ColourfulWidget, self).__init__(*args, **kwargs)
        self._index = 0
        Signals.colourfulItemAdded.connect(self.onColourfulItemAdded)
        Signals.colourfulItemAddFinished.connect(
            self.onColourfulItemAddFinished)

    def init(self):
        """初始化多彩
        """
        if self.gridLayout.count() > 0:
            return
        ColourfulThread.start(PixmapWidth, PixmapHeight)

    def doPreviewPrevious(self):
        """上一个
        """
        self._index -= 1
        self._index = max(self._index, 0)
        self.doPreview()

    def doPreviewNext(self):
        """下一个
        """
        self._index += 1
        self._index = min(self._index, self.gridLayout.count() - 1)
        self.doPreview()

    def doPreview(self):
        """主动发送预览信号
        """
        self.gridLayout.itemAt(self._index).widget().click()

    def onColourfulItemAddFinished(self):
        """添加完成
        """
        return
        # 添加一个+按钮
        self.buttonAdd = QPushButton(
            '+', self, objectName='buttonAdd', clicked=self.onAddNewColor)
        # 加载鼠标样式
        ThemeManager.loadCursor(self.buttonAdd, ThemeManager.CursorPointer)
        if self.lastCol == 4:
            self.lastCol = 0
            self.lastRow += 1
        else:
            self.lastCol += 1
        self.gridLayout.addWidget(self.buttonAdd, self.lastRow, self.lastCol)

    def onAddNewColor(self):
        """添加新颜色"""
        pass

    def onColourfulItemAdded(self, row, col, name, color):
        """
        :param row:            行
        :param col:            列
        :param name:           名字
        :param color:          颜色
        """
        self.lastRow = row
        self.lastCol = col
        self.gridLayout.addWidget(
            SkinBaseItemWidget(name, color, Signals.colourfulItemClicked, self), row, col)

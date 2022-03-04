#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Widgets.Skins.ThemeWidget
@description: 
"""

import os

from Utils.CommonUtil import Signals
from Utils.ThemeThread import ThemeThread
from Widgets.Skins.SkinBaseWidget import (PixmapHeight, PixmapWidth,
                                          SkinBaseItemWidget, SkinBaseWidget)

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ThemeWidget(SkinBaseWidget):

    def __init__(self, *args, **kwargs):
        super(ThemeWidget, self).__init__(*args, **kwargs)
        self._index = 0
        Signals.themeItemAdded.connect(self.onThemeItemAdded)
        Signals.themeItemAddFinished.connect(self.onThemeItemAddFinished)

    def init(self):
        """初始化主题
        """
        if self.gridLayout.count() > 0:
            return
        ThemeThread.start(PixmapWidth, PixmapHeight)

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
            SkinBaseItemWidget(
                name, os.path.join(os.path.dirname(path), 'preview.png'),
                Signals.themeItemClicked, self), row, col)

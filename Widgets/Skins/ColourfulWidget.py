#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.ColourfulWidget
@description: 
"""
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QPushButton

from UiFiles.Ui_ColourfulWidget import Ui_FormColourful
from Utils.CommonUtil import Signals
from Utils.ThemeManager import ThemeManager
from Utils.ThemeThread import ColourfulThread


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

PixmapWidth = 158
PixmapHeight = 152              # 图片大小
MarginBottom = 26               # 底部文字


class ColourfulItemWidget(QWidget):

    def __init__(self, name, color, *args, **kwargs):
        super(ColourfulItemWidget, self).__init__(*args, **kwargs)
        # 加载鼠标样式
        ThemeManager.loadCursor(self, ThemeManager.CursorPointer)
        self.name = name
        self.color = color
        self.hovered = False
        self.colorHover = QColor(0, 0, 0, 40)
        self.textColor = QColor(102, 102, 102)

    def mousePressEvent(self, event):
        super(ColourfulItemWidget, self).mousePressEvent(event)
        self.hovered = True
        self.textColor = QColor(18, 183, 245)
        self.update()

    def mouseReleaseEvent(self, event):
        super(ColourfulItemWidget, self).mouseReleaseEvent(event)
        self.hovered = False
        self.textColor = QColor(102, 102, 102)
        self.update()
        Signals.colourfulItemClicked.emit(self.name, self.color)

    def enterEvent(self, event):
        super(ColourfulItemWidget, self).enterEvent(event)
        self.hovered = True
        self.textColor = QColor(Qt.black)
        self.update()

    def leaveEvent(self, event):
        super(ColourfulItemWidget, self).leaveEvent(event)
        self.hovered = False
        self.textColor = QColor(102, 102, 102)
        self.update()

    def paintEvent(self, event):
        super(ColourfulItemWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # 绘制颜色方块
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawRoundedRect(
            0, 0, PixmapWidth, PixmapHeight, 2, 2)
        if self.hovered:
            # 绘制一层灰色
            painter.setBrush(QBrush(self.colorHover))
            painter.drawRoundedRect(
                0, 0, PixmapWidth, PixmapHeight, 2, 2)
        painter.restore()
        # 绘制文字
        painter.setPen(self.textColor)
        painter.drawText(0, 0, PixmapWidth, PixmapHeight + MarginBottom,
                         Qt.AlignHCenter | Qt.AlignBottom, self.name)
        painter.end()

    def sizeHint(self):
        return QSize(PixmapWidth, PixmapHeight + MarginBottom)


class ColourfulWidget(QWidget, Ui_FormColourful):

    def __init__(self, *args, **kwargs):
        super(ColourfulWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        Signals.colourfulItemAdded.connect(self.onColourfulItemAdded)
        Signals.colourfulItemAddFinished.connect(
            self.onColourfulItemAddFinished)

    def init(self):
        """初始化多彩
        """
        if self.gridLayout.count() > 0:
            return
        ColourfulThread.start(PixmapWidth, PixmapHeight)

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
            ColourfulItemWidget(name, color, self), row, col)

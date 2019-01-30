#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月27日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.SkinBaseWidget
@description: 
"""
import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget

from UiFiles.Ui_ScrollArea import Ui_FormScrollArea
from Utils.ThemeManager import ThemeManager


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

PixmapWidth = 158
PixmapHeight = 152              # 图片大小
MarginBottom = 26               # 底部文字


class SkinBaseItemWidget(QWidget):

    def __init__(self, name, colorimg, signal, *args, **kwargs):
        super(SkinBaseItemWidget, self).__init__(*args, **kwargs)
        # 加载鼠标样式
        ThemeManager.loadCursor(self, ThemeManager.CursorPointer)
        self.name = name
        self.colorimg = colorimg
        self.hovered = False
        self.signal = signal
        self.colorHover = QColor(0, 0, 0, 40)
        self.textColor = QColor(102, 102, 102)
        self.image = None
        # 图片
        if isinstance(self.colorimg, str) and os.path.isfile(self.colorimg):
            self.image = QPixmap(self.colorimg).scaled(
                PixmapWidth, PixmapHeight,
                Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

    def mousePressEvent(self, event):
        super(SkinBaseItemWidget, self).mousePressEvent(event)
        self.hovered = True
        self.textColor = QColor(18, 183, 245)
        self.update()

    def mouseReleaseEvent(self, event):
        super(SkinBaseItemWidget, self).mouseReleaseEvent(event)
        self.hovered = False
        self.textColor = QColor(102, 102, 102)
        self.update()
        self.signal.emit(self.name, self.colorimg)

    def enterEvent(self, event):
        super(SkinBaseItemWidget, self).enterEvent(event)
        self.hovered = True
        self.textColor = QColor(Qt.black)
        self.update()

    def leaveEvent(self, event):
        super(SkinBaseItemWidget, self).leaveEvent(event)
        self.hovered = False
        self.textColor = QColor(102, 102, 102)
        self.update()

    def paintEvent(self, event):
        super(SkinBaseItemWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # 绘制颜色方块
        painter.save()
        painter.setPen(Qt.NoPen)
        if self.image != None:
            # 画图片
            painter.drawPixmap(0, 0, self.image)
        else:
            # 画颜色
            painter.setBrush(QBrush(self.colorimg))
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


class SkinBaseWidget(QWidget, Ui_FormScrollArea):

    def __init__(self, *args, **kwargs):
        super(SkinBaseWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)

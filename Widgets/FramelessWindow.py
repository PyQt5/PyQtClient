#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.FramelessWindow
@description: 无边框窗口
"""
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter, QPen, QColor, QEnterEvent
from PyQt5.QtWidgets import QWidget

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FramelessWindow(QWidget):

    MARGIN = 2  # 最外层控件上下左右边距2

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self._pos = None  # 鼠标按下位置
        self._pressed = False  # 鼠标按下
        self._canmove = False  # 可以移动
        self.Direction = None  # 光标方向
        # 鼠标跟踪
        self.setMouseTracking(True)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def eventFilter(self, obj, event):
        # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(FramelessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        # 由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小
        super(FramelessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.MARGIN))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        # 鼠标按下事件记录位置
        super(FramelessWindow, self).mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            self._pos = event.pos()
            self._pressed = True
            if self.childAt(self._pos) != None:
                # 鼠标点击的位置在其它控件上
                self._canmove = True

    def mouseReleaseEvent(self, event):
        # 鼠标弹起事件
        super(FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self._canmove = False
        self.Direction = None

    def mouseDoubleClickEvent(self, event):
        # 鼠标双击事件
        super(FramelessWindow, self).mouseDoubleClickEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.childAt(self._pos) != None:
                # 鼠标点击的位置在其它控件上
                if self.isMaximized() or self.isFullScreen():
                    self.showNormal()
                else:
                    self.showMaximized()

    def mouseMoveEvent(self, event):
        # 鼠标移动事件
        super(FramelessWindow, self).mouseMoveEvent(event)

        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGIN, self.height() - self.MARGIN
        if self.isMaximized() or self.isFullScreen():
            # 最大化或者全屏则忽略
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if self._canmove:
            self.move(self.mapToGlobal(event.pos() - self._pos))
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.MARGIN and yPos <= self.MARGIN:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.MARGIN:
            # 右上角
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.MARGIN and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.MARGIN and self.MARGIN <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.MARGIN <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.MARGIN <= xPos <= wm and 0 <= yPos <= self.MARGIN:
            # 上面
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.MARGIN <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def leaveEvent(self, event):
        # 鼠标离开事件
        self.setCursor(Qt.ArrowCursor)  # 恢复鼠标形状
        super(FramelessWindow, self).leaveEvent(event)

    def changeEvent(self, event):
        # 窗口改变事件
        super(FramelessWindow, self).changeEvent(event)
        if event.type() == QEvent.WindowStateChange:  # 窗口状态改变
            state = self.windowState()
            if state == (state | Qt.WindowMaximized):
                # 最大化,要去除上下左右边界,如果不去除则边框地方会有空隙
                self.layout().setContentsMargins(0, 0, 0, 0)
            else:
                # 要保留上下左右边界,否则没有边框无法调整
                self.layout().setContentsMargins(
                    self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(FramelessWindow, self).move(pos)

    def _resizeWidget(self, pos):
        # 调整窗口大小
        if self.Direction == None:
            return
        mpos = pos - self._pos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._pos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._pos = pos
        elif self.Direction == RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._pos.setX(pos.x())
        elif self.Direction == LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._pos.setY(pos.y())
        elif self.Direction == Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._pos = pos
            else:
                return
        elif self.Direction == Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._pos = pos
            else:
                return
        self.setGeometry(x, y, w, h)

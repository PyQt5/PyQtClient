#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月29日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Widgets.Skins.PictureWidget
@description: 
"""

from PyQt5.QtCore import (QObject, QParallelAnimationGroup, QPauseAnimation,
                          QPropertyAnimation, QRectF, QSequentialAnimationGroup,
                          Qt, pyqtProperty, pyqtSignal)
from PyQt5.QtGui import QColor, QPainter
from Utils.CommonUtil import Signals
from Utils.ThemeThread import GetAllCategoryRunnable
from Widgets.Skins.SkinBaseWidget import SkinBaseItemWidget, SkinBaseWidget

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class CircleItem(QObject):

    _x = 0  # x坐标
    _opacity = 1  # 透明度0~1
    valueChanged = pyqtSignal()

    @pyqtProperty(float)
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.valueChanged.emit()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity


class PictureWidget(SkinBaseWidget):

    _waiting = False
    _circleRadius = 3  # 半径
    _circleColor = QColor(39, 174, 97)  # 圆圈颜色

    def __init__(self, category, *args, **kwargs):
        super(PictureWidget, self).__init__(*args, **kwargs)
        self._index = 0
        self.category = category
        self._items = []

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

    def showWaiting(self, show=True):
        self.setEnabled(not show)
        self._waiting = show
        if show:
            self._items.clear()
            self._initAnimations()
            for _, animation in self._items:
                animation.start()
        else:
            for _, animation in self._items:
                animation.stop()

    def addItem(self, index, title, path):
        # 计算行列
        row = int(index / 5)
        col = index % 5
        self.gridLayout.addWidget(
            SkinBaseItemWidget(title, path, Signals.pictureItemClicked, self),
            row, col)

    def init(self):
        """初始化该分类
        """
        if self.gridLayout.count() > 0:
            return
        return GetAllCategoryRunnable(self.category, self)

    def paintEvent(self, event):
        if not self._waiting:
            # 交给原来的绘制
            super(PictureWidget, self).paintEvent(event)
            return
        # 自定义绘制
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        for item, _ in self._items:
            painter.save()
            color = self._circleColor.toRgb()
            color.setAlphaF(item.opacity)
            painter.setBrush(color)
            diameter = 2 * self._circleRadius
            painter.drawRoundedRect(
                QRectF(
                    item.x / 100 * self.width() - diameter,
                    self._circleRadius / 2,
                    #                     (self.height() - self._circleRadius) / 2,
                    diameter,
                    diameter),
                self._circleRadius,
                self._circleRadius)
            painter.restore()

    def _initAnimations(self):
        for index in range(5):  # 5个小圆
            item = CircleItem(self)
            item.valueChanged.connect(self.update)
            # 串行动画组
            seqAnimation = QSequentialAnimationGroup(self)
            seqAnimation.setLoopCount(-1)
            self._items.append((item, seqAnimation))

            # 暂停延迟动画
            seqAnimation.addAnimation(QPauseAnimation(150 * index, self))

            # 加速,并行动画组1
            parAnimation1 = QParallelAnimationGroup(self)
            # 透明度
            parAnimation1.addAnimation(
                QPropertyAnimation(item,
                                   b'opacity',
                                   self,
                                   duration=400,
                                   startValue=0,
                                   endValue=1.0))
            # x坐标
            parAnimation1.addAnimation(
                QPropertyAnimation(item,
                                   b'x',
                                   self,
                                   duration=400,
                                   startValue=0,
                                   endValue=25.0))
            seqAnimation.addAnimation(parAnimation1)
            ##

            # 匀速
            seqAnimation.addAnimation(
                QPropertyAnimation(item,
                                   b'x',
                                   self,
                                   duration=2000,
                                   startValue=25.0,
                                   endValue=75.0))

            # 加速,并行动画组2
            parAnimation2 = QParallelAnimationGroup(self)
            # 透明度
            parAnimation2.addAnimation(
                QPropertyAnimation(item,
                                   b'opacity',
                                   self,
                                   duration=400,
                                   startValue=1.0,
                                   endValue=0))
            # x坐标
            parAnimation2.addAnimation(
                QPropertyAnimation(item,
                                   b'x',
                                   self,
                                   duration=400,
                                   startValue=75.0,
                                   endValue=100.0))
            seqAnimation.addAnimation(parAnimation2)
            ##

            # 暂停延迟动画
            seqAnimation.addAnimation(
                QPauseAnimation((5 - index - 1) * 150, self))

    @pyqtProperty(int)
    def circleRadius(self):
        return self._circleRadius

    @circleRadius.setter
    def circleRadius(self, radius):
        if self._circleRadius != radius:
            self._circleRadius = radius
            self.update()

    @pyqtProperty(QColor)
    def circleColor(self):
        return self._circleColor

    @circleColor.setter
    def circleColor(self, color):
        if self._circleColor != color:
            self._circleColor = color
            self.update()

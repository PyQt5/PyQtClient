#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Widgets.RubberBandButton
@description: 
"""

from PyQt5.QtCore import (QEasingCurve, QParallelAnimationGroup,
                          QPropertyAnimation, QRectF, Qt, pyqtProperty)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (QPushButton, QStyle, QStyleOptionButton,
                             QStylePainter)


class RubberBandButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super(RubberBandButton, self).__init__(*args, **kwargs)
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self._width = 0
        self._height = 0
        self._bgcolor = QColor(Qt.green)

    def paintEvent(self, event):
        self._initAnimate()
        painter = QStylePainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setBrush(QColor(self._bgcolor))
        painter.setPen(QColor(self._bgcolor))
        painter.drawEllipse(
            QRectF((self.minimumWidth() - self._width) / 2,
                   (self.minimumHeight() - self._height) / 2, self._width,
                   self._height))
        # 绘制本身的文字和图标
        options = QStyleOptionButton()
        options.initFrom(self)
        size = options.rect.size()
        size.transpose()
        options.rect.setSize(size)
        options.features = QStyleOptionButton.Flat
        options.text = self.text()
        options.icon = self.icon()
        options.iconSize = self.iconSize()
        painter.drawControl(QStyle.CE_PushButton, options)
        event.accept()

    def _initAnimate(self):
        if hasattr(self, '_animate'):
            return
        self._width = self.minimumWidth() * 7 / 8
        self._height = self.minimumHeight() * 7 / 8
        #         self._width=175
        #         self._height=175
        wanimate = QPropertyAnimation(self, b'rWidth')
        wanimate.setEasingCurve(QEasingCurve.OutElastic)
        wanimate.setDuration(700)
        wanimate.valueChanged.connect(self.update)
        wanimate.setKeyValueAt(0, self._width)
        #         wanimate.setKeyValueAt(0.1, 180)
        #         wanimate.setKeyValueAt(0.2, 185)
        #         wanimate.setKeyValueAt(0.3, 190)
        #         wanimate.setKeyValueAt(0.4, 195)
        wanimate.setKeyValueAt(0.5, self._width + 6)
        #         wanimate.setKeyValueAt(0.6, 195)
        #         wanimate.setKeyValueAt(0.7, 190)
        #         wanimate.setKeyValueAt(0.8, 185)
        #         wanimate.setKeyValueAt(0.9, 180)
        wanimate.setKeyValueAt(1, self._width)
        hanimate = QPropertyAnimation(self, b'rHeight')
        hanimate.setEasingCurve(QEasingCurve.OutElastic)
        hanimate.setDuration(700)
        hanimate.setKeyValueAt(0, self._height)
        #         hanimate.setKeyValueAt(0.1, 170)
        #         hanimate.setKeyValueAt(0.3, 165)
        hanimate.setKeyValueAt(0.5, self._height - 6)
        #         hanimate.setKeyValueAt(0.7, 165)
        #         hanimate.setKeyValueAt(0.9, 170)
        hanimate.setKeyValueAt(1, self._height)

        self._animate = QParallelAnimationGroup(self)
        self._animate.addAnimation(wanimate)
        self._animate.addAnimation(hanimate)

    def enterEvent(self, event):
        super(RubberBandButton, self).enterEvent(event)
        self._animate.stop()
        self._animate.start()

    @pyqtProperty(int)
    def rWidth(self):
        return self._width

    @rWidth.setter
    def rWidth(self, value):
        self._width = value

    @pyqtProperty(int)
    def rHeight(self):
        return self._height

    @rHeight.setter
    def rHeight(self, value):
        self._height = value

    @pyqtProperty(QColor)
    def bgColor(self):
        return self._bgcolor

    @bgColor.setter
    def bgColor(self, color):
        self._bgcolor = QColor(color)

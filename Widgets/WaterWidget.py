#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月17日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.WaterWidget
@description: 水波纹进度
"""
import math

from PyQt5.QtCore import pyqtProperty, QTimer, Qt
from PyQt5.QtGui import QColor, QPainterPath, QPainter
from PyQt5.QtWidgets import QWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class WaterWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(WaterWidget, self).__init__(*args, **kwargs)
        # 浪高百分比
        self._waterHeight = 1
        # 密度
        self._waterDensity = 1
        # 波浪颜色1
        self._waterFgColor = QColor(33, 178, 148)
        # 波浪颜色2
        self._waterBgColor = QColor(33, 178, 148, 100)
        self.minimum = 0
        self.maximum = 0
        self._value = 0
        self._offset = 0
        # 每隔100ms刷新波浪（模拟波浪动态）
        self._updateTimer = QTimer(self, timeout=self.update)
        self._updateTimer.start(100)

    def update(self):
        if self.minimum >= self.maximum:
            return
        super(WaterWidget, self).update()

    def paintEvent(self, event):
        super(WaterWidget, self).paintEvent(event)
        if self.minimum >= self.maximum:
            return
        if not self._updateTimer.isActive():
            return

        # 正弦曲线公式 y = A * sin(ωx + φ) + k
        # 当前值所占百分比
        percent = 1 - (self._value - self.minimum) / \
            (self.maximum - self.minimum)
        # w表示周期，6为人为定义
        w = 6 * self.waterDensity * math.pi / self.width()
        # A振幅 高度百分比，1/26为人为定义
        A = self.height() * self.waterHeight * 1 / 26
        # k 高度百分比
        k = self.height() * percent

        # 波浪1
        waterPath1 = QPainterPath()
        waterPath1.moveTo(0, self.height())  # 起点在左下角
        # 波浪2
        waterPath2 = QPainterPath()
        waterPath2.moveTo(0, self.height())  # 起点在左下角

        # 偏移
        self._offset += 0.6
        if self._offset > self.width() / 2:
            self._offset = 0

        for i in range(self.width() + 1):
            # 从x轴开始计算y轴点
            y = A * math.sin(w * i + self._offset) + k
            waterPath1.lineTo(i, y)

            # 相对第一条需要进行错位
            y = A * math.sin(w * i + self._offset + self.width() / 2 * A) + k
            waterPath2.lineTo(i, y)

        # 封闭两条波浪，形成一个 U形 上面加波浪的封闭区间
        waterPath1.lineTo(self.width(), self.height())
        waterPath1.lineTo(0, self.height())
        waterPath2.lineTo(self.width(), self.height())
        waterPath2.lineTo(0, self.height())

        # 开始画路径
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # 设置没有画笔
        painter.setPen(Qt.NoPen)

        # 波浪1
        painter.save()
        painter.setBrush(self._waterBgColor)
        painter.drawPath(waterPath1)
        painter.restore()

        # 波浪2
        painter.save()
        painter.setBrush(self._waterFgColor)
        painter.drawPath(waterPath2)
        painter.restore()

    def stop(self):
        self.setValue(0, 0)
        self.setRange(0, 0)
        self._updateTimer.stop()
        self.repaint()

    def value(self):
        return self._value

    def setValue(self, value, maximum=0):
        self._value = value
        if maximum > 0:
            self.maximum = maximum

    def setRange(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def setMinimum(self, minimum):
        self.minimum = minimum

    def setMaximum(self, maximum):
        self.maximum = maximum

    @pyqtProperty(float)
    def waterHeight(self):
        return self._waterHeight

    @waterHeight.setter
    def waterHeight(self, height):
        self._waterHeight = height

    @pyqtProperty(float)
    def waterDensity(self):
        return self._waterDensity

    @waterDensity.setter
    def waterDensity(self, density):
        self._waterDensity = density

    @pyqtProperty(QColor)
    def waterFgColor(self):
        return self._waterFgColor

    @waterFgColor.setter
    def waterFgColor(self, color):
        self._waterFgColor = QColor(color)

    @pyqtProperty(QColor)
    def waterBgColor(self):
        return self._waterBgColor

    @waterBgColor.setter
    def waterBgColor(self, color):
        self._waterBgColor = QColor(color)

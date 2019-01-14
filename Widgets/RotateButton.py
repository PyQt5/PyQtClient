#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.RotateButton
@description:
"""
import os

from PyQt5.QtCore import Qt, pyqtProperty, QRectF, QPropertyAnimation, QPointF
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPainterPath, QImage
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, \
    QStyleOptionButton, QStylePainter, QStyle

from Widgets.ToolTip import ToolTip


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class RotateButton(QPushButton):

    STARTVALUE = 0  # 起始旋转角度
    ENDVALUE = 360  # 结束旋转角度
    DURATION = 540  # 动画完成总时间

    def __init__(self, *args, image='', **kwargs):
        super(RotateButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)
        self._angle = 0  # 角度
        self._padding = 10  # 阴影边距
        self._image = ''  # 图片路径
        self._shadowColor = QColor(33, 33, 33)  # 阴影颜色
        self._pixmap = None  # 图片对象
        # 属性动画
        self._animation = QPropertyAnimation(self, b'angle', self)
        self._animation.setLoopCount(1)  # 只循环一次
        # 边框阴影效果
        self._effect = QGraphicsDropShadowEffect(self)
        self._effect.setBlurRadius(self._padding * 2)
        self._effect.setOffset(0, 0)
        self.setPixmap(image)
        # 绑定提示框
        ToolTip.bind(self)

    def paintEvent(self, event):
        """绘制事件"""
        text = self.text()
        option = QStyleOptionButton()
        self.initStyleOption(option)
        option.text = ''  # 不绘制文字
        painter = QStylePainter(self)
        painter.setRenderHint(QStylePainter.Antialiasing)
        painter.setRenderHint(QStylePainter.HighQualityAntialiasing)
        painter.setRenderHint(QStylePainter.SmoothPixmapTransform)
        painter.drawControl(QStyle.CE_PushButton, option)
        # 变换坐标为正中间
        painter.translate(self.rect().center())
        painter.rotate(self._angle)  # 旋转

        # 绘制图片
        if self._pixmap and not self._pixmap.isNull():
            w = self.width()
            h = self.height()
            pos = QPointF(-self._pixmap.width() / 2, -
                          self._pixmap.height() / 2)
            painter.drawPixmap(pos, self._pixmap)
        elif text:
            # 在变换坐标后的正中间画文字
            fm = self.fontMetrics()
            w = fm.width(text)
            h = fm.height()
            rect = QRectF(0 - w * 2, 0 - h, w * 2 * 2, h * 2)
            painter.drawText(rect, Qt.AlignCenter, text)
        else:
            super(RotateButton, self).paintEvent(event)

    def enterEvent(self, _):
        """鼠标进入事件"""
        # 设置阴影
        self._effect.setColor(self._shadowColor)
        self._effect.setBlurRadius(self._padding * 2)
        self.setGraphicsEffect(self._effect)

        # 开启旋转动画
        self._animation.stop()
        cv = self._animation.currentValue() or self.STARTVALUE
        self._animation.setDuration(self.DURATION if cv == 0 else int(
            cv / self.ENDVALUE * self.DURATION))
        self._animation.setStartValue(cv)
        self._animation.setEndValue(self.ENDVALUE)
        self._animation.start()

    def leaveEvent(self, _):
        """鼠标离开事件"""
        # 取消阴影
        self._effect.setBlurRadius(0)
        self.setGraphicsEffect(self._effect)

        # 旋转动画
        self._animation.stop()
        cv = self._animation.currentValue() or self.ENDVALUE
        self._animation.setDuration(int(cv / self.ENDVALUE * self.DURATION))
        self._animation.setStartValue(cv)
        self._animation.setEndValue(self.STARTVALUE)
        self._animation.start()

    def setPixmap(self, path):
        if not os.path.exists(path):
            self._image = ''
            self._pixmap = None
            return
        self._image = path
        size = min(self.width(), self.height()) - self.padding  # 需要边距的边框
        radius = int(size / 2)
        image = QImage(size, size, QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)  # 填充背景为透明
        pixmap = QPixmap(path).scaled(
            size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        # QPainter
        painter = QPainter()
        painter.begin(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # QPainterPath
        path = QPainterPath()
        path.addRoundedRect(0, 0, size, size, radius, radius)
        # 切割圆
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        self._pixmap = QPixmap.fromImage(image)
        self.update()

    def pixmap(self):
        return self._pixmap

    @pyqtProperty(str)
    def image(self):
        return self._image

    @image.setter
    def image(self, path):
        self.setPixmap(path)

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    @pyqtProperty(int)
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value

    @pyqtProperty(QColor)
    def shadowColor(self):
        return self._shadowColor

    @shadowColor.setter
    def shadowColor(self, color):
        self._shadowColor = QColor(color)

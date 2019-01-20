#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.ThemeThread
@description: 
"""
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtGui import QLinearGradient, QColor

from Utils.CommonUtil import AppLog, Signals


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ColourfulThread(QObject):
    """获取所有的颜色方案
    """

    def __init__(self, width, height, *args, **kwargs):
        super(ColourfulThread, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    @classmethod
    def start(cls, width, height, parent=None):
        """启动线程
        :param cls:
        :param width:        宽度
        :param width:        高度
        :param parent:
        """
        cls._thread = QThread(parent)
        cls._worker = ColourfulThread(width, height)
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('colourful thread started')

    def run(self):
        AppLog.info('start get all colourful')
        # 午夜巴黎
        mcolor = QLinearGradient(0, 0, self.width, self.height)
        mcolor.startColor = QColor(20, 179, 255, 255)
        mcolor.endColor = QColor(226, 14, 255, 255)
        mcolor.setColorAt(0, mcolor.startColor)
        mcolor.setColorAt(1, mcolor.endColor)
        # 樱草青葱
        pcolor = QLinearGradient(0, 0, self.width, self.height)
        pcolor.startColor = QColor(0, 173, 246, 255)
        pcolor.endColor = QColor(0, 234, 155, 255)
        pcolor.setColorAt(0, pcolor.startColor)
        pcolor.setColorAt(1, pcolor.endColor)
        # 秋日暖阳
        acolor = QLinearGradient(0, 0, self.width, self.height)
        acolor.startColor = QColor(255, 128, 27, 255)
        acolor.endColor = QColor(255, 0, 14, 255)
        acolor.setColorAt(0, acolor.startColor)
        acolor.setColorAt(1, acolor.endColor)

        defaults = self.splistList([
            [self.tr('MidnightParis'), mcolor],             # 午夜巴黎
            [self.tr('PrimroseGreenOnion'), pcolor],        # 樱草青葱
            [self.tr('AutumnSun'), acolor],                 # 秋日暖阳
            [self.tr('LightGray'), QColor(236, 236, 236)],  # 淡灰色
            [self.tr('DarkBlack'), QColor(33, 33, 33)],     # 深黑色
            [self.tr('BlueGreen'), QColor(0, 190, 172)],    # 蓝绿色
            [self.tr('Orange'), QColor(255, 152, 0)],       # 橙色
            [self.tr('Brown'), QColor(140, 100, 80)],       # 咖啡色
            [self.tr('Green'), QColor(121, 190, 60)],       # 绿色
            [self.tr('Pink'), QColor(236, 98, 161)],        # 粉色
            [self.tr('Purple'), QColor(103, 58, 183)],      # 紫色
            [self.tr('Blue'), QColor(0, 188, 212)],         # 蓝色
            [self.tr('GreyBlue'), QColor(80, 126, 164)],    # 蓝灰色
            [self.tr('Red'), QColor(244, 94, 99)],          # 红色
        ], 5)

        for row, default in enumerate(defaults):
            for col, (name, color) in enumerate(default):
                Signals.colourfulItemAdded.emit(row, col, name, color)
                QThread.msleep(100)
                QThread.yieldCurrentThread()

        Signals.colourfulItemAddFinished.emit()
        AppLog.info('colourful thread end')

    def splistList(self, src, length):
        # 等分列表
        return [src[i:i + length] for i in range(len(src)) if i % length == 0]

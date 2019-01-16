#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月13日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.StyledItemDelegate
@description: 自定义进度条委托
"""
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QStyledItemDelegate

from Utils import Constants


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class StyledItemDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        super(StyledItemDelegate, self).paint(painter, option, index)
        if index.data(Constants.RoleRoot):
            value = index.data(Constants.RoleValue)
            total = index.data(Constants.RoleTotal)
            if value == None or total == None or (value >= total) or total == 0:
                return
            # 绘制进度条
            painter.setPen(QPen(self.parent().barColor, 1))
            painter.drawLine(
                QPointF(option.rect.x(), option.rect.y() +
                        option.rect.height()),
                QPointF(option.rect.width() * value / total,
                        option.rect.y() + option.rect.height())
            )

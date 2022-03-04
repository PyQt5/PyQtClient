#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Dialogs.MoveDialog
@description: 可移动对话框
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog
from Utils.CommonUtil import qBound


class MoveDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(MoveDialog, self).__init__(*args, **kwargs)
        self._pos = None
        self._rect = QApplication.instance().desktop().availableGeometry(self)

    def mousePressEvent(self, event):
        super(MoveDialog, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._pos = event.pos()

    def mouseReleaseEvent(self, event):
        super(MoveDialog, self).mouseReleaseEvent(event)
        self._pos = None
        # 限制移动到屏幕外
        #         x = qBound(0, self.x(), self._rect.width() - self.width())
        y = qBound(0, self.y(),
                   self._rect.height() - int(2 * self.height() / 3))
        #         self.move(x, y)
        self.move(self.x(), y)

    def mouseMoveEvent(self, event):
        super(MoveDialog, self).mouseMoveEvent(event)
        if not self._pos:
            return
        if self.isMaximized() or self.isFullScreen():
            return
        pos = event.pos() - self._pos
        x = self.x() + pos.x()
        y = self.y() + pos.y()
        self.move(x, y)

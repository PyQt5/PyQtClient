#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.ToolTip
@description: 仿QToolTip
"""
from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class ToolTip(QWidget):

    _instance = None
    TimeOut = 2000

    def __init__(self, *args, **kwargs):
        super(ToolTip, self).__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags() |
                            Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setVisible(False)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        # 定时隐藏
        self._hideTimer = QTimer(self, timeout=self.hide)

    @classmethod
    def bind(cls, widget):
        if not cls._instance:
            cls._instance = cls()
        widget.installEventFilter(cls._instance)

    def setText(self, text):
        self.label.setText(text)

    def eventFilter(self, widget, event):
        #         if isinstance(event, QHelpEvent):
        #             self.hide()
        #             self._hideTimer.stop()
        #             self.setText(widget.toolTip())
        #             if not widget.toolTip():
        #                 return True
        #             self.show()
        #             # 自动隐藏
        #             self._hideTimer.start(self.TimeOut)
        #             pos = widget.mapToGlobal(QPoint(0, 0))
        #             self.move(pos.x() + widget.width() + 30,
        #                       pos.y() + int((widget.height() - self.height()) / 2))
        #             return True
        t = event.type()
        if t == QEvent.Enter:           # 鼠标进入
            self.hide()
            self._hideTimer.stop()
            self.setText(widget.toolTip())
            if widget.toolTip():
                self.show()
                # 自动隐藏
                self._hideTimer.start(self.TimeOut)
                pos = widget.mapToGlobal(QPoint(0, 0))
                self.move(pos.x() + widget.width() + 30,
                          pos.y() + int((widget.height() - self.height()) / 2))
        elif t == QEvent.Leave:         # 鼠标离开
            self._hideTimer.stop()
            self.hide()

        return super(ToolTip, self).eventFilter(widget, event)

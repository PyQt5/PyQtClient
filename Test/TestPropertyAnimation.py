#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestPropertyAnimation
@description: 
"""
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('start', self, clicked=self.onStart))
        layout.addWidget(QPushButton('pause', self, clicked=self.onPause))
        layout.addWidget(QPushButton('resume', self, clicked=self.onResume))

        self._offset = 0
        self.pani = QPropertyAnimation(self, b'offset', self)
        self.pani.setDuration(540)
        self.pani.setLoopCount(1)
        self.pani.setStartValue(0)
        self.pani.setEndValue(360)

    def onPause(self):
        self.pani.stop()
        v = self.pani.currentValue()
        print('current value:', v, 'duration:', int(v / 360 * 540))
        self.pani.setDuration(int(v / 360 * 540))
        self.pani.setStartValue(v)
        self.pani.setEndValue(0)

    def onResume(self):
        self.pani.start()

    def onStart(self):
        self.pani.start()

    @pyqtProperty(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, o):
        print(o)
        self._offset = o


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

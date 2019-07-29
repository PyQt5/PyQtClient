#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.tSlotsByName
@description:
"""
import sys

from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout

from Widgets.Buttons.RotateButton import RotateButton


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class Ui_FormMainWindow(object):

    def setupUi(self, FormMainWindow):
        layout = QVBoxLayout(FormMainWindow)
        layout.addWidget(RotateButton('test', FormMainWindow, objectName='buttonTest'))
        QMetaObject.connectSlotsByName(FormMainWindow)


class FrameWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(FrameWindow, self).__init__(*args, **kwargs)


class WindowBase:

    @pyqtSlot()
    def on_buttonTest_clicked(self):
        print('clicked')


class Window(FrameWindow, WindowBase, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

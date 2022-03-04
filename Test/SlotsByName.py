#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.tSlotsByName
@description:
"""

import sys

from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from Widgets.Buttons.RotateButton import RotateButton


class Ui_FormMainWindow(object):

    def setupUi(self, FormMainWindow):
        layout = QVBoxLayout(FormMainWindow)
        layout.addWidget(
            RotateButton('test', FormMainWindow, objectName='buttonTest'))
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

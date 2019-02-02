#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestFestivalStyle
@description: 
"""
from time import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget

from UiFiles.Ui_MainWindow import Ui_FormMainWindow
from Utils.ThemeManager import ThemeManager


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class Window(QWidget, Ui_FormMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setupUi(self)
        self.buttonClose.clicked.connect(self.close)
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonMinimum.clicked.connect(self.showMinimized)
        self.buttonNormal.clicked.connect(self.showNormal)
        t = time()
        ThemeManager.loadTheme()
        print(time() - t)
        ThemeManager.loadCursor(self)
        ThemeManager.loadCursor(self.buttonHead, ThemeManager.CursorPointer)


if __name__ == '__main__':
    import sys
    import os
    os.chdir('../')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.resize(800, 770)
    w.show()

    lw = QListWidget()
    lw.show()
    lw.addItems(os.listdir('Resources/Images/Festival'))

    def setStyle(item):
        path = os.path.join('Resources/Images/Festival', item.text(), 'background.jpg')
        if os.path.isfile(path):
            ThemeManager.loadPictureTheme(path)
    lw.itemClicked.connect(setStyle)

    sys.exit(app.exec_())

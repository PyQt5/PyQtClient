#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestMainwindowStyle
@description: 
"""
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
        ThemeManager.loadTheme()
        ThemeManager.loadCursor(self)
        ThemeManager.loadCursor(self.buttonHead, 'pointer.png')


if __name__ == '__main__':
    import sys
    import os
    os.chdir('../')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.resize(800, 770)
    w.show()
    w.grab().save('Resources/Themes/Default/preview.png')

    lw = QListWidget()
    lw.show()
    lw.addItems(os.listdir('Resources/Themes'))

    def setStyle(item):
        path = os.path.join('Resources/Themes', item.text(), 'style.qss')
        if os.path.isfile(path):
            ThemeManager.loadUserTheme(item.text())
            w.grab().save('Resources/Themes/{}/preview.png'.format(item.text()))
    lw.itemClicked.connect(setStyle)

    sys.exit(app.exec_())

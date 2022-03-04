#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file:
@description:
"""

import os

import win32api
import win32con
import win32gui
from PyQt5.QtWidgets import QApplication, QWidget


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        c = win32gui.LoadImage(None, os.path.abspath('cursor.ani'),
                               win32con.IMAGE_CURSOR, 0, 0,
                               win32con.LR_LOADFROMFILE)
        print(c)
        win32api.SetClassLong(int(self.winId()), win32con.GCL_HCURSOR, c)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    print(app.topLevelWindows())
    print(int(app.topLevelWindows()[0].winId()), int(w.winId()))
    print(app.focusWidget())
    print(app.focusWindow())
    print(app.allWidgets())
    print(app.allWindows())
    app.setActiveWindow(w)
    print(app.activeWindow())
    sys.exit(app.exec_())

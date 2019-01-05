#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file:
@description:
"""
import os

from PyQt5.QtWidgets import QWidget, QApplication
import win32api
import win32con
import win32gui

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        c = win32gui.LoadImage(
            None,
            os.path.abspath('cursor.ani'),
            win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE
        )
        print(c)
        win32api.SetClassLong(
            int(self.winId()),
            win32con.GCL_HCURSOR, c)


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

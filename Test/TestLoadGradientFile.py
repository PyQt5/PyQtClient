#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年2月1日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestLoadGradientFile
@description: 
"""
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QLinearGradient
from PyQt5.QtWidgets import QWidget

from Utils.GradientUtils import GradientUtils


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)

        setting = QSettings('gradient.ini', QSettings.IniFormat)
        setting.setIniCodec('UTF-8')

        gradient = setting.value('gradient')
        print(gradient)
        if gradient:
            gradient = GradientUtils.toGradient(gradient)
            print(gradient)
            gradient = GradientUtils.styleSheetCode(gradient)
            print(gradient)
            self.setStyleSheet('background: {};'.format(gradient))

        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, Qt.red)
        gradient.setColorAt(0.5, Qt.green)
        gradient.setColorAt(1, Qt.blue)

        gradient = GradientUtils.toJson(gradient)
        print(gradient)
        setting.setValue('gradient', gradient)
        setting.sync()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

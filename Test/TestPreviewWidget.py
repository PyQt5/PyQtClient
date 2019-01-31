#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月30日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestPreviewWidget
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Utils.ThemeManager import ThemeManager
from Widgets.Skins.PreviewWidget import PreviewWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

if __name__ == '__main__':
    import sys
    import os
    import cgitb
    os.chdir('../')
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ThemeManager.loadTheme()
    w = PreviewWidget()
    w.show()
    w.setTitle('Test')
    w.setPixmap(QPixmap(
        'Resources/Themes/Default/preview.png').scaledToWidth(400, Qt.SmoothTransformation))
    sys.exit(app.exec_())

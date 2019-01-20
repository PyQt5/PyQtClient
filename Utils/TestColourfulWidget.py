#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.TestColourfulWidget
@description: 
"""
from Utils.CommonUtil import Signals
from Widgets.Skins.ColourfulWidget import ColourfulWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

if __name__ == '__main__':
    import sys
    import os
    os.chdir('../')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(
        'ColourfulWidget{background:white;}\n#scrollArea,#scrollAreaWidgetContents{background:transparent;}')
    w = ColourfulWidget()
    Signals.colourfulItemClicked.connect(
        lambda name, colors: print(name, colors))
    w.show()
    w.init()
    sys.exit(app.exec_())

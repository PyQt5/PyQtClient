#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月17日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestWaterWidget
@description: 
"""
from Widgets.WaterWidget import WaterWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet("""WaterWidget {
        min-width: 260px;
        max-width: 260px;
        background: rgba(39, 174, 97, 255);    /*背景颜色*/
        qproperty-waterHeight: 0.8;
        qproperty-waterFgColor: rgba(255, 255, 255, 80);
        qproperty-waterBgColor: rgba(255, 255, 255, 50);
    }
    """)
    w = WaterWidget()
    w.setRange(0, 100)
    w.setValue(50)
    w.show()
    sys.exit(app.exec_())

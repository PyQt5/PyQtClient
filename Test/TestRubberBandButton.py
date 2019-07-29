#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestRubberBandButton
@description: 
"""

from Widgets.Buttons.RubberBandButton import RubberBandButton


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    RubberBandButton {
        min-width: 200px;
        max-width: 200px;
        min-height: 200px;
        max-height: 200px;
        border: none;
        color: white;
        outline: none;
        margin: 4px;
        qproperty-bgColor: rgba(255, 0, 0, 150);
    }
    """)
    w = QWidget()
    w.resize(800, 600)
    layout = QHBoxLayout(w)
    layout.addWidget(RubberBandButton('hello', w))
    w.show()
    sys.exit(app.exec_())
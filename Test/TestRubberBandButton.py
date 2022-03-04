#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestRubberBandButton
@description: 
"""

from Widgets.Buttons.RubberBandButton import RubberBandButton

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget
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

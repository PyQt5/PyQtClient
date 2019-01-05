#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月2日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestToolTip
@description: 
"""
from PyQt5.QtWidgets import QWidget

from Widgets.ToolTip import ToolTip


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class TestWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        btn1 = QPushButton('鼠标悬停1', self, minimumHeight=38, toolTip='这是按钮1')
        ToolTip.bind(btn1)
        layout.addWidget(btn1)

        btn2 = QPushButton('鼠标悬停2', toolTip='这是按钮2')
        ToolTip.bind(btn2)
        layout.addWidget(btn2)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton
    app = QApplication(sys.argv)
    app.setStyleSheet("""ToolTip > QLabel {
    color: white;
    border-radius: 5px;
    padding: 10px;
    background-color: rgba(77, 77, 77, 180);
    }""")
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())

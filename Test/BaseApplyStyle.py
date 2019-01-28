#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月28日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.BaseApplyStyle
@description: 
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton,\
    QApplication


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class StyleWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(StyleWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.editStyle = QPlainTextEdit(self)
        layout.addWidget(self.editStyle)
        layout.addWidget(QPushButton('Apply', self, clicked=self.onApply))
        self.editStyle.setPlainText(QApplication.instance().styleSheet())

    def onApply(self):
        QApplication.instance().setStyleSheet(self.editStyle.toPlainText())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = StyleWindow()
    w.show()
    sys.exit(app.exec_())

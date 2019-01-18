#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.RunCode
@description: 过滤排序Model
"""
import os
import runpy
import sys
import traceback


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


def escape(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&#x27;")
    s = s.replace('\n', '<br/>')
    s = s.replace(' ', '&nbsp;')
    return s


def showError(message):
    from PyQt5.QtWidgets import QApplication, QErrorMessage, QCheckBox, \
        QPushButton, QLabel, QStyle
    from PyQt5.QtCore import Qt
    QApplication.addLibraryPath('./Qt/plugins')
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    # 设置内置错误图标
    app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxCritical))
    w = QErrorMessage()
    w.finished.connect(lambda _: app.quit)
    w.resize(600, 400)
    # 去掉右上角?
    w.setWindowFlags(w.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    w.setWindowTitle(w.tr('Error'))
    # 隐藏图标、勾选框、按钮
    w.findChild(QLabel, '').setVisible(False)
    w.findChild(QCheckBox, '').setVisible(False)
    w.findChild(QPushButton, '').setVisible(False)
    w.showMessage(escape(message))
    sys.exit(app.exec_())


def runCode(file):
    """运行文件
    :param file:              python file
    """
    try:
        dirPath = os.path.dirname(file)
        sys.argv = [file]
        sys.path.insert(0, dirPath)
        os.chdir(dirPath)
        runpy.run_path(file, run_name='__main__')
    except SystemExit:
        pass
    except:
        showError(traceback.format_exc())

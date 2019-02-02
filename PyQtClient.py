#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月1日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: PyQtClient
@description:
"""

from distutils.sysconfig import get_python_lib
import os
import sys
import traceback


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

sys.path.append(os.path.abspath('Library.zip'))

libpath = get_python_lib()
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    libpath, 'PyQt5', 'Qt', 'plugins', 'platforms')
os.environ['QML_IMPORT_PATH'] = os.path.join(libpath, 'Qt', 'qml')
os.environ['QML2_IMPORT_PATH'] = os.environ['QML_IMPORT_PATH']

if os.name == 'nt':
    os.environ['PATH'] = os.path.join(
        libpath, 'PyQt5', 'Qt', 'bin') + os.pathsep + os.environ['PATH']
os.environ['PATH'] = os.path.dirname(
    os.path.abspath(sys.argv[0])) + os.pathsep + os.environ['PATH']

print(os.environ['PATH'])


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


try:
    from Widgets import MainWindow
    MainWindow.main()
except SystemExit:
    pass
except:
    showError(traceback.format_exc())

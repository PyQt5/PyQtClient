#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月1日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: PyQtClient
@description:
"""

import os
import sys
from distutils.sysconfig import get_python_lib

from rich.console import Console
from rich.terminal_theme import NIGHT_OWLISH

sys.path.append(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.abspath('Library.zip'))

libpath = get_python_lib()
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    libpath, 'PyQt5', 'Qt', 'plugins', 'platforms')
os.environ['QML_IMPORT_PATH'] = os.path.join(libpath, 'Qt', 'qml')
os.environ['QML2_IMPORT_PATH'] = os.environ['QML_IMPORT_PATH']

if os.name == 'nt':
    os.environ['PATH'] = os.path.join(libpath, 'PyQt5', 'Qt',
                                      'bin') + os.pathsep + os.environ['PATH']
os.environ['PATH'] = os.path.dirname(os.path.abspath(
    sys.argv[0])) + os.pathsep + os.environ['PATH']


def showError(message):
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QApplication, QCheckBox, QErrorMessage, QFrame,
                                 QLabel, QPushButton, QStyle, QTextEdit)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    # 设置内置错误图标
    app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxCritical))
    w = QErrorMessage()
    w.setStyleSheet('QErrorMessage { background-color: white; }')
    w.finished.connect(lambda _: app.quit)
    w.resize(950, 790)
    # 去掉右上角?
    w.setWindowFlags(w.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    w.setWindowTitle(w.tr('Error'))
    # 隐藏图标、勾选框、按钮
    w.findChild(QLabel, '').setVisible(False)
    w.findChild(QCheckBox, '').setVisible(False)
    w.findChild(QPushButton, '').setVisible(False)
    edit = w.findChild(QTextEdit, '')
    edit.setFrameShape(QFrame.NoFrame)
    edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    w.showMessage(message)
    sys.exit(app.exec_())


def do_analysis():
    from Widgets import MainWindow
    try:
        # 获取函数调用图
        from pycallgraph2.config import Config
        from pycallgraph2.globbing_filter import GlobbingFilter
        from pycallgraph2.output.graphviz import GraphvizOutput
        from pycallgraph2.pycallgraph import PyCallGraph

        # 函数流程图调用
        config = Config()
        config.trace_filter = GlobbingFilter(
            include=['Widgets.*', 'Utils.*'],
            exclude=['pycallgraph2.*', '*.secret_function'])
        with PyCallGraph(GraphvizOutput(tool='dot',
                                        output_file='call_detail.png'),
                         config=config):
            MainWindow.main()
    except Exception:
        MainWindow.main()


try:
    if '-analysis' in sys.argv:
        do_analysis()
    else:
        from Widgets import MainWindow
        MainWindow.main()
except SystemExit:
    pass
except Exception:
    console = Console(record=True)
    console.print_exception(max_frames=5)
    showError(console.export_html(theme=NIGHT_OWLISH, inline_styles=True))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestSkinDialog
@description: 
"""

from Utils.CommonUtil import initLog
from Utils.Constants import LogName
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.SkinDialog import SkinDialog

from Test.BaseApplyStyle import StyleWindow

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

if __name__ == '__main__':
    import cgitb
    import os
    import sys
    os.chdir('../')
    sys.excepthook = cgitb.enable(1, None, 5, '')

    initLog(LogName)

    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = SkinDialog()
    ThemeManager.loadTheme()
    w.show()
    ww = StyleWindow()
    ww.show()
    sys.exit(app.exec_())

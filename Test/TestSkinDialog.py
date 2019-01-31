#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestSkinDialog
@description: 
"""
from Test.BaseApplyStyle import StyleWindow
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.SkinDialog import SkinDialog
from Utils.CommonUtil import initLog
from Utils.Constants import LogName


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


if __name__ == '__main__':
    import sys
    import os
    import cgitb
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
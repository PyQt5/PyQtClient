#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: PyQtClient
@description: 
"""

import os

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

executable = os.path.abspath('pythonw.exe')
file = os.path.abspath('PyQtClient.pyw')
os.execl(executable, executable, *[file])

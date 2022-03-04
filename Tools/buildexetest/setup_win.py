#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: setup_win
@description: 
"""

import sys
from distutils.core import setup

import py2exe  # @UnusedImport

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

sys.path.append('../')

# windows 无控制台
# console  有控制台

sys.argv.append('py2exe')  # 允许程序通过双击的形式执行

includes = []
excludes = []
dll_excludes = []

# compressed 为1 则压缩文件
# optimize 为优化级别 默认为0
options = {
    'py2exe': {
        'compressed': 1,
        'optimize': 2,
        'bundle_files': 0,
        'includes': includes,
        'excludes': excludes,
        'dll_excludes': dll_excludes
    }
}

setup(version='1.0',
      description='PyQtClient',
      name='PyQtClient',
      zipfile=None,
      options=options,
      windows=[{
          'script': 'PyQtClient.py',
          'icon_resources': [(1, 'app.ico')],
      }],
      data_files=[])

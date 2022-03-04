#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018年3月29日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: Ui2Py
@description: 转换UI文件
"""

import os
import sys
from pathlib import Path

for p in Path('../UiFiles').rglob('*.ui'):
    path, ext = os.path.splitext(os.path.abspath(str(p)))
    fname = os.path.basename(path)
    path = os.path.dirname(path)
    dst = os.path.join(path, 'Ui_' + fname + '.py')
    command = '{0} -m PyQt5.uic.pyuic --from-imports -x -o {1} {2}'.format(
        sys.executable, dst, os.path.abspath(str(p)))
    os.system(command)

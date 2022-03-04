#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.buildzip
@description: 
"""

import os
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

os.chdir('../')

# 压缩文件到zip
zipfp = ZipFile(os.path.abspath('Library.zip'), 'w', ZIP_DEFLATED)
for file in Path('Library').rglob('*.pyc'):
    print('add file: %s' % file)
    zipfp.write(os.path.abspath(str(file)), str(file)[len('Library'):])
zipfp.close()

shutil.rmtree('Library', ignore_errors=True)

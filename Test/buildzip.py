#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.buildzip
@description: 
"""

import os
from pathlib import Path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED


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

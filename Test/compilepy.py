#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.compilepy
@description: 
"""

import compileall
import os
from pathlib import Path
import shutil
import sys


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

os.chdir('../')

# 删除Library目录
dirPath = os.path.abspath('Library')

shutil.rmtree(dirPath, ignore_errors=True)

# 创建目录
os.makedirs(dirPath, exist_ok=True)
# 复制目录
shutil.copytree(os.path.abspath('UiFiles'),
                os.path.join(dirPath, 'UiFiles'))
shutil.copytree(os.path.abspath('Utils'), os.path.join(dirPath, 'Utils'))
shutil.copytree(os.path.abspath('Dialogs'),
                os.path.join(dirPath, 'Dialogs'))
shutil.copytree(os.path.abspath('Widgets'),
                os.path.join(dirPath, 'Widgets'))

open(os.path.join(dirPath, '__init__.py'), 'wb').write(b'')

# 编译整个目录
compileall.compile_dir(dirPath, force=True, optimize=0)


info = sys.version_info
cpythonname = '.cpython-{}{}'.format(info.major, info.minor)
print(cpythonname)

for file in Path(dirPath).rglob('*.pyc'):
    path = os.path.join(str(file.parent.parent), file.name)
    shutil.copy(str(file), path)
    try:
        os.rename(path, path.replace(cpythonname, ''))
    except:
        pass

# 删除py文件和ui文件,pyd文件
for ext in ('*.py', '*.ui', '*.pyd', '*.bak'):
    for file in Path(dirPath).rglob(ext):
        try:
            os.unlink(str(file))
        except Exception as e:
            print(e)
for file in Path(dirPath).rglob('__pycache__'):
    try:
        shutil.rmtree(str(file), ignore_errors=True)
    except Exception as e:
        print(e)

print('编译完成')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月29日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: GenerateLanguage
@description: 生成多语言文件
"""
import os


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"

os.chdir('../')

fp = open('PyQtClient.pro', 'wb')

fp.write(b'SOURCES         = PyQtClient.py\\\n')
for path in ('UiFiles', 'Utils', 'Widgets'):
    for name in os.listdir(path):
        if name.find('__init__') > -1 or not name.endswith('.py'):
            continue
        fp.write('                  {}/{}\\\n'.format(path, name).encode())

fp.write(b'\n')
fp.write(b'FORMS         = ')
path = 'UiFiles'
for name in os.listdir(path):
    if not name.endswith('.ui'):
        continue
    fp.write('                  {}/{}\\\n'.format(path, name).encode())

fp.write(b'\n')
fp.write(b'TRANSLATIONS    = app_zh_CN.ts\n')
fp.write(b'CODECFORTR      = UTF-8\n')
fp.write(b'CODECFORSRC     = UTF-8\n')

print('ok')

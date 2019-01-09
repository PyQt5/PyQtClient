#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Test.TestSetting
@description: 
"""
import os

from PyQt5.QtCore import QVariant

from Utils.CommonUtil import Setting


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

os.chdir('../')

print(Setting.value('accounts', [], QVariant))

Setting.setValue('accounts', ['892768447@qq.com'])

print(Setting.value('accounts', [], QVariant))
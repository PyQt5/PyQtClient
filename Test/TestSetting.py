#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test.TestSetting
@description: 
"""

import os

from PyQt5.QtCore import QVariant
from Utils.CommonUtil import Setting

os.chdir('../')

print(Setting.value('accounts', [], QVariant))

Setting.setValue('accounts', ['892768447@qq.com'])

print(Setting.value('accounts', [], QVariant))

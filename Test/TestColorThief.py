#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Utils.ColorThief import ColorThief


# Created on 2019年1月29日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: Test.TestColorThief
# description: 
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

# 获取图片主色调
color_thief = ColorThief(r'C:\Users\89276\Desktop\春节.jpg')
color = color_thief.get_color()

print(color)
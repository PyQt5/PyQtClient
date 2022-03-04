#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.ColorThief import ColorThief

# 获取图片主色调
color_thief = ColorThief(r'C:\Users\89276\Desktop\春节.jpg')
color = color_thief.get_color()

print(color)

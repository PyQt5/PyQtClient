#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.PictureWidget
@description: 
"""
from PyQt5.QtWidgets import QTabWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class PictureWidget(QTabWidget):

    def __init__(self, *args, **kwargs):
        super(PictureWidget, self).__init__(*args, **kwargs)

    def init(self):
        """初始化下载图片
        """
        pass

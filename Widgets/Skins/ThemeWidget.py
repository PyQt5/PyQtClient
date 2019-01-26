#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.Skins.ThemeWidget
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from UiFiles.Ui_ScrollArea import Ui_FormScrollArea


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ThemeWidget(QWidget, Ui_FormScrollArea):

    def __init__(self, *args, **kwargs):
        super(ThemeWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def init(self):
        """初始化主题
        """
        if self.gridLayout.count() > 0:
            return

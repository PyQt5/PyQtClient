#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月11日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.DonateDialog
@description: 捐赠对话框
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Widgets.Dialogs.MoveDialog import MoveDialog
from UiFiles.Ui_DonateDialog import Ui_FormDonateDialog
from Utils.ThemeManager import ThemeManager


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class DonateDialog(MoveDialog, Ui_FormDonateDialog):

    def __init__(self, alipayImg, wechatImg, *args, **kwargs):
        super(DonateDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 关闭后自动销毁
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 加载鼠标样式
        ThemeManager.loadCursor(self)
        # 加载鼠标样式
        ThemeManager.loadCursor(self.labelAlipayImg)
        ThemeManager.loadCursor(self.labelWechatImg, 'pointer.png')
        # 加载图片
        self.labelAlipayImg.setPixmap(QPixmap(alipayImg).scaled(
            300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.labelWechatImg.setPixmap(QPixmap(wechatImg).scaled(
            300, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

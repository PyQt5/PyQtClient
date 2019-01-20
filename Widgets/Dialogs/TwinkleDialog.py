#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.TwinkleDialog
@description: windows 对话框边框闪烁
"""
import os

from PyQt5.QtWidgets import QDialog

if os.name == 'nt':
    import ctypes.wintypes

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

WM_NCACTIVATE = 0x0086


class TwinkleDialog:

    def setTarget(self, widget):
        """设置闪烁的目标控件
        :param widget:        目标控件
        """
        self._targetWidget = widget
        self._targetWidget.setProperty('_active', True)

    def activeAnimation(self, actived):
        """边框闪烁动画
        :param actived: 是否激活
        """
        if not hasattr(self, '_targetWidget'):
            return
        self._targetWidget.setProperty('_active', actived)
        # 刷新样式
        self.style().polish(self._targetWidget)

    if os.name == 'nt':

        def nativeEvent(self, eventType, message):
            retval, result = QDialog.nativeEvent(self, eventType, message)
            if eventType == 'windows_generic_MSG' and hasattr(self, '_targetWidget'):
                msg = ctypes.wintypes.MSG.from_address(message.__int__())
                if msg.message == WM_NCACTIVATE:
                    # 绘制模态窗口的边框效果
                    self.activeAnimation(msg.wParam == 1)
            return retval, result

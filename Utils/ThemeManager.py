#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.ThemeManager
@description: 主题管理
"""
import os

from PyQt5.QtCore import QSettings, QTextCodec
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

from Utils.CommonUtil import AppLog

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class ThemeManager:

    ThemeDir = 'Resources/Themes'
    ThemeName = 'Default'

    @classmethod
    def loadTheme(cls, parent=None):
        """根据配置加载主题
        :param cls:
        :param parent:
        """
        setting = QSettings('Resources/Data/Config.ini',
                            QSettings.IniFormat, parent)
        setting.setIniCodec(QTextCodec.codecForName('utf-8'))
        cls.ThemeName = setting.value('theme', 'Default', str)
        # 加载动态光标(windows)
#         path = cls.cursorPath()
#         AppLog.info('cursorPath: {}'.format(path))
#         if os.path.exists(path) and os.name == 'nt':
#             import win32gui
#             import win32api
#             import win32con
#             cursor = win32gui.LoadImage(
#                 None, path,
#                 win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE
#             )
#             AppLog.info('cursor handle: {}'.format(cursor))
#             if cursor != None and cursor > 0:
#                 win32api.SetClassLong(int(QApplication.instance().allWidgets()[0].winId()), win32con.GCL_HCURSOR, cursor)
        # 加载主题中的字体
        path = cls.fontPath()
        AppLog.info('fontPath: {}'.format(path))
        if os.path.exists(path):
            QFontDatabase.addApplicationFont(path)
        # 加载主题取样式
        path = cls.stylePath()
        AppLog.info('stylePath: {}'.format(path))
        try:
            QApplication.instance().setStyleSheet(open(path, 'rb').read().decode('utf-8'))
        except Exception as e:
            AppLog.error(str(e))

    @classmethod
    def cursorPath(cls):
        """
        :param cls:
        :return: 主题中 cursor.ani 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'cursor.ani'))

    @classmethod
    def fontPath(cls):
        """
        :param cls:
        :return: 主题中 font.ttf 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'font.ttf'))

    @classmethod
    def stylePath(cls):
        """
        :param cls:
        :return: 主题中 style.qss 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'style.qss'))

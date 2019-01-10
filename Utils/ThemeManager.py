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
from PyQt5.QtGui import QFontDatabase, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication

from Utils.CommonUtil import AppLog
from Utils.Constants import ConfigFile


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
        setting = QSettings(ConfigFile,
                            QSettings.IniFormat, parent)
        setting.setIniCodec(QTextCodec.codecForName('utf-8'))
        cls.ThemeName = setting.value('theme', 'Default', str)
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
    def loadCursor(cls, parent, name='default.png'):
        # 加载光标
        path = cls.cursorPath(name)
        AppLog.info('cursorPath: {}'.format(path))
        if os.path.exists(path):
            # 设置自定义鼠标样式,并以0,0为原点
            parent.setCursor(QCursor(QPixmap(path), 0, 0))

    @classmethod
    def cursorPath(cls, name='default.png'):
        """
        :param cls:
        :return: 主题中 default.png 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'cursor', name)).replace('\\', '/')

    @classmethod
    def setPointerCursors(cls, parent):
        """设置部分指定控件的鼠标样式
        :param cls:
        """
        path = os.path.abspath(os.path.join(
            cls.ThemeDir, cls.ThemeName, 'cursor', 'pointer.png')).replace('\\', '/')
        if os.path.exists(path):
            cursor = QCursor(QPixmap(path), 0, 0)
            parent.buttonHead.setCursor(cursor)         # 主界面头像
            parent.buttonGithub.setCursor(cursor)       # Github按钮
            parent.buttonQQ.setCursor(cursor)           # QQ按钮
            parent.buttonGroup.setCursor(cursor)        # 群按钮
            parent.buttonBackToUp.setCursor(cursor)     # 返回顶部按钮

    @classmethod
    def fontPath(cls):
        """
        :param cls:
        :return: 主题中 font.ttf 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'font.ttf')).replace('\\', '/')

    @classmethod
    def stylePath(cls):
        """
        :param cls:
        :return: 主题中 style.qss 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'style.qss')).replace('\\', '/')

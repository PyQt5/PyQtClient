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

from PyQt5.QtGui import QFontDatabase, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication

from Utils.ColorThief import ColorThief
from Utils.CommonUtil import AppLog, Setting


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

StyleTemplate = """
#widgetMain {{
    border-image: url({0});    /*背景图片*/
}}

/*工具栏*/
#widgetTools {{
    background-color: rgba(38, 38, 38, 10);
}}

/*存放网页控件*/
#widgetContents {{
    background: rgba(248, 248, 248, 150);
}}

/*搜索框中的按钮*/
#buttonSearch {{
    qproperty-bgColor: rgb({1}, {2}, {3}, 255);
}}

/*返回顶部,主页按钮*/
#buttonBackToUp, #buttonHome {{
    qproperty-bgColor: rgb({1}, {2}, {3}, 255);
}}

/*工具栏中的按钮*/
#buttonGithub, #buttonQQ, #buttonGroup {{
    background: rgb({1}, {2}, {3}, 255);
}}

/*登录窗口*/
#widgetLogin {{
    background: rgb({1}, {2}, {3}, 210);
}}

/*激活状态*/
#widgetLogin[_active="true"] {{
    border: 1px solid rgba({1}, {2}, {3}, 255);
}}
"""


class ThemeManager:

    ThemeDir = 'Resources/Themes'
    ThemeName = 'Default'

    # 鼠标
    CursorDefault = 'default.png'
    CursorPointer = 'pointer.png'

    @classmethod
    def loadTheme(cls):
        """根据配置加载主题
        :param cls:
        :param parent:
        """
        cls.ThemeName = Setting.value('theme', 'Default', str)
        # 加载主题中的字体
        path = cls.fontPath()
        AppLog.info('fontPath: {}'.format(path))
        if os.path.isfile(path):
            QFontDatabase.addApplicationFont(path)
        # 加载主题取样式
        path = cls.stylePath()
        AppLog.info('stylePath: {}'.format(path))
        try:
            QApplication.instance().setStyleSheet(
                open(path, 'rb').read().decode('utf-8', errors='ignore'))
            return 1
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadUserTheme(cls, theme='Default'):
        """加载主题目录里的主题
        :param cls:
        :param theme:        文件夹名字
        """
        cls.ThemeName = theme
        if cls.loadTheme():
            Setting.setValue('theme', theme)

    @classmethod
    def loadColourfulTheme(cls, color):
        """基于当前设置主题颜色
        :param cls:
        :param color:        背景颜色
        """
        pass

    @classmethod
    def loadPictureTheme(cls, image=None):
        """设置图片背景的主题
        :param cls:
        :param image:         背景图片
        """
        cls.ThemeName = Setting.value('theme', 'Default', str)
        # 加载主题取样式
        path = cls.stylePath()
        AppLog.info('stylePath: {}'.format(path))
        try:
            styleSheet = open(path, 'rb').read().decode(
                'utf-8', errors='ignore')
            # 需要替换部分样式
            if image and os.path.isfile(image):
                # 获取图片主色调
                color_thief = ColorThief(image)
                color = color_thief.get_color()
                AppLog.info('dominant color: {}'.format(str(color)))
                styleSheet += StyleTemplate.format(
                    os.path.abspath(image).replace('\\', '/'),
                    *color)
            QApplication.instance().setStyleSheet(styleSheet)
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadCursor(cls, widget, name='default.png'):
        # 加载光标
        path = cls.cursorPath(name)
        AppLog.info('cursorPath: {}'.format(path))
        if os.path.exists(path):
            # 设置自定义鼠标样式,并以0,0为原点
            widget.setCursor(QCursor(QPixmap(path), 0, 0))

    @classmethod
    def cursorPath(cls, name='default.png'):
        """
        :param cls:
        :return: 主题中 鼠标图片 的绝对路径
        """
        return os.path.abspath(os.path.join(cls.ThemeDir, cls.ThemeName, 'cursor', name)).replace('\\', '/')

    @classmethod
    def setPointerCursors(cls, widgets):
        """设置部分指定控件的鼠标样式
        :param cls:
        """
        path = os.path.abspath(os.path.join(
            cls.ThemeDir, cls.ThemeName, 'cursor', cls.CursorPointer)).replace('\\', '/')
        if os.path.exists(path):
            cursor = QCursor(QPixmap(path), 0, 0)
            for w in widgets:
                w.setCursor(cursor)

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

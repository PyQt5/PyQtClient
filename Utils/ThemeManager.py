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

from PyQt5.QtGui import QFontDatabase, QCursor, QPixmap, QLinearGradient,\
    QRadialGradient, QConicalGradient
from PyQt5.QtWidgets import QApplication

from Utils.ColorThief import ColorThief
from Utils.CommonUtil import AppLog, Setting
from Utils.GradientUtils import GradientUtils


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

# 修改背景图片
StylePictureTemplate = """
/*主窗口*/
#widgetMain {{
    border-image: url({0});    /*背景图片*/
}}
"""

# 修改颜色
StyleColorTemplate = """
/*主窗口*/
#widgetMain {{
    background-color: rgba({0}, {1}, {2}, 255);
}}

/*搜索框中的按钮*/
#buttonSearch {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/*工具栏*/
#widgetTools {{
    background-color: rgba({0}, {1}, {2}, 20);
}}

/*工具栏中的按钮*/
#buttonGithub, #buttonQQ, #buttonGroup {{
    background: rgba({0}, {1}, {2}, 255);
}}

/*返回顶部,主页按钮*/
#buttonBackToUp, #buttonHome {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/*存放网页控件*/
#widgetContents {{
    background: rgba(248, 248, 248, 200);
}}

/*登录窗口*/
#widgetLogin {{
    background: rgba({0}, {1}, {2}, 210);
}}

/*激活状态*/
#widgetLogin[_active="true"] {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/*捐赠,更新,错误,主题窗口*/
#widgetDonate, #widgetUpdate, #widgetError, #widgetSkin {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
    background: rgba({0}, {1}, {2}, 255);    /*背景颜色*/
}}

/*捐赠窗口,更新窗口,错误,主题窗口背景*/
#widgetImage, #widgetUpdateBg, #widgetErrorBg, #widgetSkinBg {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/*更新进度条*/
#progressBarUpdate::chunk {{
    background-color: rgba({0}, {1}, {2}, 255);
}}

/*pip按钮*/
#buttonInstall {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:hover {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:pressed {{
    background: rgba({0}, {1}, {2}, 255);
}}

#tabWidgetSkinMain > QTabBar::tab:selected {{
    color: rgb({0}, {1}, {2});
    border-bottom: 2px solid rgb({0}, {1}, {2});
}}

#widgetCategories > QPushButton:checked {{
    color: rgb({0}, {1}, {2});
}}

#sliderOpacity::groove:horizontal {{
    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba({0}, {1}, {2}, 255), stop:1 rgba(255, 255, 255, 255));
}}
#sliderOpacity::handle:horizontal {{
    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.9 rgba(255, 255, 255, 255), stop:1 rgba({0}, {1}, {2}, 255));
}}

/*壁纸控件进度条*/
PictureWidget {{
    /*圆圈颜色*/
    qproperty-circleColor: rgb({0}, {1}, {2});
}}

/*主题界面中缩略图控件文字悬停颜色*/
#skinBaseItemWidget {{
    qproperty-textHoverColor: rgb({0}, {1}, {2});
}}

#buttonPreviewApply {{
    background: rgb({0}, {1}, {2});
}}
#buttonPreviewApply:hover {{
    background: rgba({0}, {1}, {2}, 200);
}}
#buttonPreviewApply:pressed {{
    background: rgba({0}, {1}, {2}, 230);
}}
"""

# 渐变颜色
StyleGradientTemplate = """
/*主窗口*/
#widgetMain {{
    background-color: {3};
}}

/*搜索框中的按钮*/
#buttonSearch {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/*工具栏*/
#widgetTools {{
    background-color: rgba({0}, {1}, {2}, 20);
}}

/*工具栏中的按钮*/
#buttonGithub, #buttonQQ, #buttonGroup {{
    background: rgba({0}, {1}, {2}, 255);
}}

/*返回顶部,主页按钮*/
#buttonBackToUp, #buttonHome {{
    qproperty-bgColor: rgba({0}, {1}, {2}, 255);
}}

/*存放网页控件*/
#widgetContents {{
    background: rgba(248, 248, 248, 200);
}}

/*登录窗口*/
#widgetLogin {{
    background: {3};
}}

/*激活状态*/
#widgetLogin[_active="true"] {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/*捐赠,更新,错误,主题窗口*/
#widgetDonate, #widgetUpdate, #widgetError, #widgetSkin {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
    background: {3};    /*背景颜色*/
}}

/*捐赠窗口,更新窗口,错误,主题窗口背景*/
#widgetImage, #widgetUpdateBg, #widgetErrorBg, #widgetSkinBg {{
    border: 1px solid rgba({0}, {1}, {2}, 255);
}}

/*更新进度条*/
#progressBarUpdate::chunk {{
    background-color: {3};
}}

/*pip按钮*/
#buttonInstall {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:hover {{
    background: rgba({0}, {1}, {2}, 255);
}}
#buttonInstall:pressed {{
    background: rgba({0}, {1}, {2}, 255);
}}

#tabWidgetSkinMain > QTabBar::tab:selected {{
    color: rgb({0}, {1}, {2});
    border-bottom: 2px solid rgb({0}, {1}, {2});
}}

#widgetCategories > QPushButton:checked {{
    color: rgb({0}, {1}, {2});
}}

#sliderOpacity::groove:horizontal {{
    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba({0}, {1}, {2}, 255), stop:1 rgba(255, 255, 255, 255));
}}
#sliderOpacity::handle:horizontal {{
    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.9 rgba(255, 255, 255, 255), stop:1 rgba({0}, {1}, {2}, 255));
}}

/*壁纸控件进度条*/
PictureWidget {{
    /*圆圈颜色*/
    qproperty-circleColor: rgb({0}, {1}, {2});
}}

/*主题界面中缩略图控件文字悬停颜色*/
#skinBaseItemWidget {{
    qproperty-textHoverColor: rgb({0}, {1}, {2});
}}

#buttonPreviewApply {{
    background: rgb({0}, {1}, {2});
}}
#buttonPreviewApply:hover {{
    background: rgba({0}, {1}, {2}, 200);
}}
#buttonPreviewApply:pressed {{
    background: rgba({0}, {1}, {2}, 230);
}}
"""


class ThemeManager:

    ThemeDir = 'Resources/Themes'
    ThemeName = 'Default'

    # 鼠标
    CursorDefault = 'default.png'
    CursorPointer = 'pointer.png'

    # 鼠标图片缓存
    Cursors = {}

    @classmethod
    def styleSheet(cls):
        """获取Application的样式
        """
        return QApplication.instance().styleSheet()

    @classmethod
    def loadTheme(cls):
        """根据配置加载主题
        :param cls:
        :param parent:
        """
        ThemeManager.ThemeName = Setting.value('theme', 'Default', str)
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
        Setting.setValue('theme', theme)
        cls.loadTheme()

    @classmethod
    def loadColourfulTheme(cls, color, widget=None):
        """基于当前设置主题颜色
        :param cls:
        :param color:        背景颜色
        :param widget:        指定控件
        """
        ThemeManager.ThemeName = 'Default'
        # 加载主题取样式
        path = cls.stylePath()
        AppLog.info('stylePath: {}'.format(path))
        try:
            styleSheet = open(path, 'rb').read().decode(
                'utf-8', errors='ignore')
            # 需要替换部分样式
            colorstr = GradientUtils.styleSheetCode(color)
            if isinstance(color, QLinearGradient) or isinstance(color, QRadialGradient) or isinstance(color, QConicalGradient):
                color = color.stops()[0][1]
            styleSheet += StyleGradientTemplate.format(
                color.red(), color.green(), color.blue(), colorstr)
            widget = widget or QApplication.instance()
            widget.setStyleSheet(styleSheet)
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadPictureTheme(cls, image=None, widget=None):
        """设置图片背景的主题
        :param cls:
        :param image:         背景图片
        :param widget:        指定控件
        """
        ThemeManager.ThemeName = Setting.value('theme', 'Default', str)
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
                styleSheet += StylePictureTemplate.format(os.path.abspath(
                    image).replace('\\', '/')) + StyleColorTemplate.format(*color)
            widget = widget or QApplication.instance()
            widget.setStyleSheet(styleSheet)
        except Exception as e:
            AppLog.exception(e)

    @classmethod
    def loadCursor(cls, widget, name='default.png'):
        # 加载光标
        path = cls.cursorPath(name)
        if path in ThemeManager.Cursors:
            widget.setCursor(ThemeManager.Cursors[path])
            return
        AppLog.info('cursorPath: {}'.format(path))
        if os.path.exists(path):
            # 设置自定义鼠标样式,并以0,0为原点
            cur = QCursor(QPixmap(path), 0, 0)
            ThemeManager.Cursors[path] = cur
            widget.setCursor(cur)

    @classmethod
    def cursorPath(cls, name='default.png'):
        """
        :param cls:
        :return: 主题中 鼠标图片 的绝对路径
        """
        return os.path.abspath(os.path.join(ThemeManager.ThemeDir, ThemeManager.ThemeName, 'cursor', name)).replace('\\', '/')

    @classmethod
    def setPointerCursors(cls, widgets):
        """设置部分指定控件的鼠标样式
        :param cls:
        """
        path = os.path.abspath(os.path.join(
            ThemeManager.ThemeDir, ThemeManager.ThemeName, 'cursor', cls.CursorPointer)).replace('\\', '/')
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
        return os.path.abspath(os.path.join(ThemeManager.ThemeDir, ThemeManager.ThemeName, 'font.ttf')).replace('\\', '/')

    @classmethod
    def stylePath(cls):
        """
        :param cls:
        :return: 主题中 style.qss 的绝对路径
        """
        return os.path.abspath(os.path.join(ThemeManager.ThemeDir, ThemeManager.ThemeName, 'style.qss')).replace('\\', '/')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月20日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.ThemeThread
@description: 
"""
import os
from pathlib import Path

from PyQt5.QtCore import QObject, QThread, QRunnable
from PyQt5.QtGui import QLinearGradient, QColor
import requests

from Utils.CommonUtil import AppLog, Signals
from Utils.Constants import DirThemes, UrlGetAllCategoriesV2,\
    UrlGetAppsByCategory, DirImages


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"

Headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6824.400 QQBrowser/10.3.3137.400'
}


def splistList(src, length):
    # 等分列表
    return [src[i:i + length] for i in range(len(src)) if i % length == 0]


class ColourfulThread(QObject):
    """获取所有的颜色方案
    """

    def __init__(self, width, height, *args, **kwargs):
        super(ColourfulThread, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    @classmethod
    def start(cls, width, height, parent=None):
        """启动线程
        :param cls:
        :param width:        宽度
        :param width:        高度
        :param parent:
        """
        cls._thread = QThread(parent)
        cls._worker = ColourfulThread(width, height)
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('colourful thread started')

    def run(self):
        AppLog.info('start get all colourful')
        # 午夜巴黎
        mcolor = QLinearGradient(0, 0, self.width, self.height)
        mcolor.startColor = QColor(20, 179, 255, 255)
        mcolor.endColor = QColor(226, 14, 255, 255)
        mcolor.setColorAt(0, mcolor.startColor)
        mcolor.setColorAt(1, mcolor.endColor)
        # 樱草青葱
        pcolor = QLinearGradient(0, 0, self.width, self.height)
        pcolor.startColor = QColor(0, 173, 246, 255)
        pcolor.endColor = QColor(0, 234, 155, 255)
        pcolor.setColorAt(0, pcolor.startColor)
        pcolor.setColorAt(1, pcolor.endColor)
        # 秋日暖阳
        acolor = QLinearGradient(0, 0, self.width, self.height)
        acolor.startColor = QColor(255, 128, 27, 255)
        acolor.endColor = QColor(255, 0, 14, 255)
        acolor.setColorAt(0, acolor.startColor)
        acolor.setColorAt(1, acolor.endColor)

        defaults = splistList([
            [self.tr('MidnightParis'), mcolor],             # 午夜巴黎
            [self.tr('PrimroseGreenOnion'), pcolor],        # 樱草青葱
            [self.tr('AutumnSun'), acolor],                 # 秋日暖阳
            [self.tr('LightGray'), QColor(236, 236, 236)],  # 淡灰色
            [self.tr('DarkBlack'), QColor(33, 33, 33)],     # 深黑色
            [self.tr('BlueGreen'), QColor(0, 190, 172)],    # 蓝绿色
            [self.tr('Orange'), QColor(255, 152, 0)],       # 橙色
            [self.tr('Brown'), QColor(140, 100, 80)],       # 咖啡色
            [self.tr('Green'), QColor(121, 190, 60)],       # 绿色
            [self.tr('Pink'), QColor(236, 98, 161)],        # 粉色
            [self.tr('Purple'), QColor(103, 58, 183)],      # 紫色
            [self.tr('Blue'), QColor(0, 188, 212)],         # 蓝色
            [self.tr('GreyBlue'), QColor(80, 126, 164)],    # 蓝灰色
            [self.tr('Red'), QColor(244, 94, 99)],          # 红色
        ], 5)

        for row, default in enumerate(defaults):
            for col, (name, color) in enumerate(default):
                Signals.colourfulItemAdded.emit(row, col, name, color)
                QThread.msleep(100)
                QThread.yieldCurrentThread()

        Signals.colourfulItemAddFinished.emit()
        AppLog.info('colourful thread end')


class ThemeThread(QObject):
    """获取所有的主题（本地和云端）
    """

    def __init__(self, width, height, *args, **kwargs):
        super(ThemeThread, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    @classmethod
    def start(cls, width, height, parent=None):
        """启动线程
        :param cls:
        :param width:        宽度
        :param width:        高度
        :param parent:
        """
        cls._thread = QThread(parent)
        cls._worker = ThemeThread(width, height)
        cls._worker.moveToThread(cls._thread)
        cls._thread.started.connect(cls._worker.run)
        cls._thread.finished.connect(cls._worker.deleteLater)
        cls._thread.start()
        AppLog.info('theme thread started')

    def run(self):
        AppLog.info('start get all theme')

        defaults = [[p.parent.name, str(p)]
                    for p in Path(DirThemes).rglob('style.qss')]

        defaults = splistList(defaults, 5)

        for row, default in enumerate(defaults):
            for col, (name, path) in enumerate(default):
                Signals.themeItemAdded.emit(row, col, name, path)
                QThread.msleep(100)
                QThread.yieldCurrentThread()

        Signals.themeItemAddFinished.emit()
        AppLog.info('theme thread end')


class GetAllCategoriesRunnable(QRunnable):

    def __init__(self, *args, **kwargs):
        super(GetAllCategoriesRunnable, self).__init__(*args, **kwargs)
        self.setAutoDelete(True)

    def run(self):
        categories = []
        try:
            req = requests.get(UrlGetAllCategoriesV2)
            content = req.json()
            categories = content.get('data', [])
            AppLog.debug('errmsg: %s', content.get('errmsg', ''))
            AppLog.debug('consume: %s', content.get('consume', ''))
            AppLog.debug('total: %s', content.get('total', ''))
        except Exception as e:
            AppLog.exception(e)
        Signals.getCategoriesFinished.emit(categories)


class GetAllCategoryRunnable(QRunnable):

    def __init__(self, cid, widget, *args, **kwargs):
        super(GetAllCategoryRunnable, self).__init__(*args, **kwargs)
        self.setAutoDelete(True)
        self.cid = cid
        self.widget = widget

    def download(self, index, url):
        try:
            dirPath = os.path.join(DirImages, self.cid)
            os.makedirs(dirPath, exist_ok=True)
            req = requests.get(url, headers=Headers)
            if req.status_code == 200:
                path = os.path.join(dirPath, os.path.basename(url))
                with open(path, 'wb') as fp:
                    fp.write(req.content)
                self.pictureDownloadFinished.emit(self, index, path)
        except Exception as e:
            AppLog.exception(e)

    def run(self):
        datas = []
        try:
            req = requests.get(UrlGetAppsByCategory.format(
                cid=self.cid, start=0, count=200))
            content = req.json()
            datas = content.get('data', [])
            AppLog.debug('errmsg: %s', content.get('errmsg', ''))
            AppLog.debug('consume: %s', content.get('consume', ''))
            AppLog.debug('total: %s', content.get('total', ''))
            # 加载前20个
            for i, item in enumerate(datas[:20]):
                url = item.get('url', None)
                if not url:
                    continue
                self.download(i, url)
        except Exception as e:
            AppLog.exception(e)
        Signals.getCategoryFinished.emit(self.widget, datas)

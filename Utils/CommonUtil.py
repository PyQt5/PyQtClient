#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月3日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.CommonUtil
@description: 公共工具类
"""
import hashlib
import logging
import os

from PyQt5.QtCore import QSettings, QTextCodec, QObject, pyqtSignal

from Utils.Constants import LogName, LogFormatterDebug, LogFormatter, ConfigFile


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


def qBound(miv, cv, mxv):
    return max(min(cv, mxv), miv)


def git_blob_hash(path):
    """git方式计算文件sha1
    :param path: file path
    """
    data = open(path, 'rb').read().replace(b'\r\n', b'\n')
    data = b'blob ' + str(len(data)).encode() + b'\0' + data
    return hashlib.sha1(data).hexdigest()


def initLog(name, file=None, level=logging.DEBUG, formatter=None):
    """初始化日志记录配置
    :param name:            log name
    :param file:            log file
    :param level:           log level
    :param formatter:       log formatter
    """

    formatter = formatter or logging.Formatter(
        LogFormatterDebug if level == logging.DEBUG else LogFormatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file = os.path.abspath(str(file))
    if file and os.path.exists(file):
        file_handler = logging.FileHandler(file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


AppLog = logging.getLogger(LogName)


class Setting:

    _Setting = None

    @classmethod
    def init(cls, parent=None):
        """初始化配置实例
        :param cls:
        :param parent:
        """
        if not cls._Setting:
            cls._Setting = QSettings(ConfigFile, QSettings.IniFormat, parent)
            cls._Setting.setIniCodec(QTextCodec.codecForName('utf-8'))

    @classmethod
    def value(cls, key, default=None, typ=None):
        """获取配置中的值
        :param cls:
        :param key:        键名
        :param default:    默认值
        :param typ:        类型
        """
        cls.init()
        if default != None and typ != None:
            return cls._Setting.value(key, default, typ)
        if default != None:
            return cls._Setting.value(key, default)
        return cls._Setting.value(key)

    @classmethod
    def setValue(cls, key, value):
        """更新配置中的值
        :param cls:
        :param key:        键名
        :param value:      键值
        """
        cls.init()
        cls._Setting.setValue(key, value)
        cls._Setting.sync()


class _Signals(QObject):

    # 运行例子信号
    runExampled = pyqtSignal(str)
    # 过滤筛选目录
    filterChanged = pyqtSignal(str)

    # 登录失败
    loginErrored = pyqtSignal(str)
    # 登录成功发送用户的id和昵称
    loginSuccessed = pyqtSignal(str, str)


# 说白了就是全局信号定义
Signals = _Signals()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月10日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.NetworkAccessManager
@description: 网页网络请求类
"""
import mimetypes
import os
import webbrowser

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager

from Utils import Constants
from Utils.CommonUtil import AppLog, Signals


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

class NetworkAccessManager(QNetworkAccessManager):

    def __init__(self, *args, **kwargs):
        super(NetworkAccessManager, self).__init__(*args, **kwargs)

    def createRequest(self, op, originalReq, outgoingData):
        """创建请求
        :param op:           操作类型见http://doc.qt.io/qt-5/qnetworkaccessmanager.html#Operation-enum
        :param originalReq:  原始请求
        :param outgoingData: 输出数据
        """
        url = originalReq.url()
        surl = url.toString()
        AppLog.debug('access url: {}'.format(surl))

        if surl.endswith('Donate'):
            # 点击了打赏
            originalReq.setUrl(QUrl())
            return super(NetworkAccessManager, self).createRequest(op, originalReq, outgoingData)
        elif surl.endswith('k=5QVVEdF'):
            # 点击了QQ群链接
            webbrowser.open(Constants.UrlGroup)
            originalReq.setUrl(QUrl())
            return super(NetworkAccessManager, self).createRequest(op, originalReq, outgoingData)

        if url.scheme() == 'tencent':
            # 调用tx的app
            webbrowser.open(surl)
            originalReq.setUrl(QUrl())
        elif url.scheme() == 'file':
            # 本地文件,比如一些图片文件等
            name = surl.split('Markdown/')
            if len(name) > 1:
                name = name[1]
                path = os.path.join(
                    Constants.DirCurrent, name).replace('\\', '/')
                if os.path.exists(path) and os.path.isfile(path):
                    if name[-3:] == '.py':
                        originalReq.setUrl(QUrl())
                        # 运行py文件
                        Signals.runExampled.emit(path)
                    else:
                        originalReq.setUrl(QUrl.fromLocalFile(path))
        else:
            # 只加载文件,不加载其它网页
            if not mimetypes.guess_type(url.fileName())[0]:
                originalReq.setUrl(QUrl())
                # 调用系统打开网页
                webbrowser.open_new_tab(surl)

        return super(NetworkAccessManager, self).createRequest(op, originalReq, outgoingData)

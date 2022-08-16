#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月10日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Utils.NetworkAccessManager
@description: 网页网络请求类
"""
import mimetypes
import os
import re
import webbrowser

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager

from Utils import Constants
from Utils.CommonUtil import AppLog, Signals


class NetworkAccessManager(QNetworkAccessManager):

    def __init__(self, *args, **kwargs):
        super(NetworkAccessManager, self).__init__(*args, **kwargs)
        self.whitelist = re.compile(r'codebeat.co|shields.io')

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
            return super(NetworkAccessManager,
                         self).createRequest(op, originalReq, outgoingData)
        elif surl.endswith('k=5QVVEdF'):
            # 点击了QQ群链接
            webbrowser.open(Constants.UrlGroup)
            originalReq.setUrl(QUrl())
            return super(NetworkAccessManager,
                         self).createRequest(op, originalReq, outgoingData)
        elif self.whitelist.search(surl):
            return super(NetworkAccessManager,
                         self).createRequest(op, originalReq, outgoingData)
        elif surl.find('#') > -1:
            originalReq.setUrl(QUrl())
            Signals.anchorJumped.emit(
                re.split(r'#\d+[,.，。、]|#\d+', surl, 1)[-1].strip())
            return super(NetworkAccessManager,
                         self).createRequest(op, originalReq, outgoingData)

        if url.scheme() == 'tencent':
            # 调用tx的app
            webbrowser.open(surl)
            originalReq.setUrl(QUrl())
        elif url.scheme() == 'file':
            # 本地文件,比如一些图片文件等
            names = surl.split('Markdown/')
            if len(names) > 1:
                rname = names[1]
                path = os.path.join(Constants.DirCurrent,
                                    rname).replace('\\', '/')
                if os.path.exists(path) and os.path.isfile(path):
                    if rname[-3:] == '.py':
                        originalReq.setUrl(QUrl())
                        # 运行py文件
                        Signals.runExampled.emit(path)
                    elif rname[-3:] == '.ui':
                        originalReq.setUrl(QUrl())
                        # 运行ui文件
                        Signals.runUiFile.emit(path)
                    else:
                        originalReq.setUrl(QUrl.fromLocalFile(path))
                elif os.path.exists(path) and os.path.isdir(path):
                    if rname.count('/') == 0:
                        # 跳转到左侧目录树
                        originalReq.setUrl(QUrl())
                        Signals.itemJumped.emit(rname)
        else:
            # 只加载文件,不加载其它网页
            if not mimetypes.guess_type(url.fileName())[0]:
                originalReq.setUrl(QUrl())
                # 调用系统打开网页
                webbrowser.open_new_tab(surl)

        return super(NetworkAccessManager,
                     self).createRequest(op, originalReq, outgoingData)

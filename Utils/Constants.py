#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.Constants
@description:
"""
from PyQt5.QtNetwork import QNetworkRequest


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

ProjectRepo = 'PyQt5/PyQt'
ConfigFile = 'Resources/Data/Config.ini'

LogName = 'PyQtClient'
LogFormatterDebug = '[%(asctime)s %(name)s %(module)s:%(funcName)s:%(lineno)s] %(levelname)-8s %(message)s'
LogFormatter = '[%(asctime)s %(name)s] %(levelname)-8s %(message)s'
LogFile = 'Resources/Data/app.log'

DirErrors = 'Resources/Data/Errors'
DirProjects = 'Resources/Data/Projects'

AttrCallback = QNetworkRequest.User + 1
AttrFilePath = QNetworkRequest.User + 2
UrlProject = 'https://github.com/PyQt5/PyQtClient'
UrlQQ = 'tencent://message/?uin=892768447'
UrlGroup = 'tencent://groupwpa/?subcmd=all&param=7B2267726F757055696E223A3234363236393931392C2274696D655374616D70223A313531383537323831357D0A'
UrlHomePage = 'https://api.github.com/repos/PyQt5/PyQt/contents'

# Github Api访问实例
_Github = None
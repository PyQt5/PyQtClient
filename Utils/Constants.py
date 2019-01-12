#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.Constants
@description: 常量
"""

from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QNetworkRequest


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"

RoleFile = Qt.UserRole + 1
RoleName = Qt.UserRole + 2
RolePath = Qt.UserRole + 3

HomeFile = 'Resources/Markdown/index.html'

ProjectRepo = 'PyQt5/PyQt'
ConfigFile = 'Resources/Data/Config.ini'

ImageDir = 'Resources/Images/Avatars'
ImageAvatar = 'Resources/Images/Avatars/avatar.png'

LogName = 'PyQtClient'
LogFormatterDebug = '[%(asctime)s %(name)s %(module)s:%(funcName)s:%(lineno)s] %(levelname)-8s %(message)s'
LogFormatter = '[%(asctime)s %(name)s] %(levelname)-8s %(message)s'
LogFile = 'Resources/Data/app.log'

DirErrors = 'Resources/Data/Errors'         # 错误日志目录
DirProjects = 'Resources/Data/Projects'     # 本地项目目录
DirCurrent = 'Resources/Data/Projects'      # 当前README.md目录
CurrentReadme = ''                          # 当前加载的README.md路径

AttrCallback = QNetworkRequest.User + 1
AttrFilePath = QNetworkRequest.User + 2
UrlProject = 'https://github.com/PyQt5/PyQtClient'
UrlQQ = 'tencent://message/?uin=892768447'
UrlGroup = 'tencent://groupwpa/?subcmd=all&param=7B2267726F757055696E223A3234363236393931392C2274696D655374616D70223A313531383537323831357D0A'
UrlHomePage = 'https://api.github.com/repos/PyQt5/PyQt/contents'

# Github Api访问实例
_Github = None
_Account = ''
_Passord = ''
_Username = ''

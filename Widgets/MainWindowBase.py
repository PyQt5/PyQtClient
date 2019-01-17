#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Widgets.MainWindowBase
@description: 
"""
import os
import webbrowser

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage

from Utils import Constants
from Utils.CommonUtil import Signals
from Utils.NetworkAccessManager import NetworkAccessManager
from Utils.ThemeManager import ThemeManager
from Widgets.ToolTip import ToolTip


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class MainWindowBase:

    def _initUi(self):
        """初始UI"""
        self.setupUi(self)
        # 隐藏还原按钮
        self.buttonNormal.setVisible(False)
        # 隐藏目录树的滑动条
        self.treeViewCatalogs.verticalScrollBar().setVisible(False)
        # 加载主题
        ThemeManager.loadTheme()
        # 加载鼠标样式
        ThemeManager.loadCursor(self.widgetMain)
        ThemeManager.setPointerCursors([
            self.buttonHead,            # 主界面头像
            self.buttonSearch,          # 主界面搜索按钮
            self.buttonGithub,          # Github按钮
            self.buttonQQ,              # QQ按钮
            self.buttonGroup,           # 群按钮
            self.buttonBackToUp,        # 返回顶部按钮
            self.buttonHome             # 显示主页readme
        ])
        # 安装事件过滤器用于还原鼠标样式
        self.widgetMain.installEventFilter(self)
        # 绑定返回顶部提示框
        ToolTip.bind(self.buttonBackToUp)
        ToolTip.bind(self.buttonHome)
        # 头像提示控件
        ToolTip.bind(self.buttonHead)

    def _initSignals(self):
        """初始化信号槽"""
        self.webViewContent.loadFinished.connect(self._exposeInterface)
        self.webViewContent.linkClicked.connect(self.onLinkClicked)
        # 绑定信号槽
        Signals.showReadmed.connect(self.renderReadme)
        Signals.urlLoaded.connect(self.onUrlLoaded)
        Signals.runExampled.connect(self._runFile)
        Signals.cloneFinished.connect(self.treeViewCatalogs.initCatalog)
        Signals.cloneFinished.connect(self.renderReadme)
        Signals.progressStoped.connect(self.widgetCatalogs.stop)
        Signals.progressUpdated.connect(self.widgetCatalogs.setValue)
        Signals.updateDialogShowed.connect(self._initUpdate)

    def _initWebView(self):
        """初始化网页"""
        settings = self.webViewContent.settings()
        # 设置默认编码
        settings.setDefaultTextEncoding('UTF-8')
        # 开启开发人员工具
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        page = self.webViewContent.page()
        # 设置链接可以点击
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        # 使用自定义的网络请求类(方便处理一些链接点击)
        page.setNetworkAccessManager(NetworkAccessManager(self.webViewContent))

        # 加载readme
        self.webViewContent.load(QUrl.fromLocalFile(
            os.path.abspath(Constants.HomeFile)))

    @pyqtSlot()
    def on_buttonSkin_clicked(self):
        """选择主题样式
        """
        pass

    @pyqtSlot()
    def on_buttonIssues_clicked(self):
        """提交意见
        """
        webbrowser.open_new_tab(Constants.UrlIssues)

    @pyqtSlot()
    def on_buttonMinimum_clicked(self):
        """最小化
        """
        self.showMinimized()

    @pyqtSlot()
    def on_buttonMaximum_clicked(self):
        """最大化
        """
        self.showMaximized()

    @pyqtSlot()
    def on_buttonNormal_clicked(self):
        """还原
        """
        self.showNormal()

    @pyqtSlot()
    def on_buttonClose_clicked(self):
        """关闭
        """
        self.close()

    @pyqtSlot()
    def on_buttonHead_clicked(self):
        """点击头像
        """
        if Constants._Account != '' and Constants._Password != '':
            self.renderReadme()
        else:
            self.initLogin()

    def on_lineEditSearch_textChanged(self, text):
        """过滤筛选
        """
        return
        Signals.filterChanged.emit(text)

    @pyqtSlot()
    def on_buttonSearch_clicked(self):
        """点击搜索按钮
        """
        pass

    @pyqtSlot()
    def on_buttonGithub_clicked(self):
        """点击项目按钮
        """
        webbrowser.open_new_tab(Constants.UrlProject)

    @pyqtSlot()
    def on_buttonQQ_clicked(self):
        """点击QQ按钮
        """
        webbrowser.open(Constants.UrlQQ)

    @pyqtSlot()
    def on_buttonGroup_clicked(self):
        """点击群按钮
        """
        webbrowser.open(Constants.UrlGroup)

    @pyqtSlot()
    def on_buttonBackToUp_clicked(self):
        """点击返回按钮
        """
        self._runJs('backToUp();')

    @pyqtSlot()
    def on_buttonHome_clicked(self):
        """主页readme
        """
        self.renderReadme()

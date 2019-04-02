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

from PyQt5.QtCore import pyqtSlot, QUrl, QLocale, QTranslator
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QApplication, QMenu, QAction

from Utils import Constants
from Utils.CommonUtil import Signals, Setting, AppLog, openFolder
from Utils.GradientUtils import GradientUtils
from Utils.NetworkAccessManager import NetworkAccessManager
from Utils.ThemeManager import ThemeManager
from Widgets.Dialogs.SkinDialog import SkinDialog
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
        # 加载鼠标样式
        ThemeManager.loadCursor(self.widgetMain)
        ThemeManager.setPointerCursors([
            self.buttonHead,            # 主界面头像
            self.buttonClear,           # 主界面清空按钮
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
        # 加载主题
        colourful = Setting.value('colourful')
        picture = Setting.value('picture', '', str)
        AppLog.debug('colourful: %s', str(colourful))
        AppLog.debug('picture: %s', picture)
        if picture:
            ThemeManager.loadFont()
            ThemeManager.loadPictureTheme(picture)
        elif colourful:
            ThemeManager.loadFont()
            if isinstance(picture, QColor):
                ThemeManager.loadColourfulTheme(colourful)
            else:
                # json数据转渐变
                ThemeManager.loadColourfulTheme(
                    GradientUtils.toGradient(colourful))
        else:
            ThemeManager.loadTheme()

    def _initSignals(self):
        """初始化信号槽"""
        self.webViewContent.loadFinished.connect(self._exposeInterface)
        self.webViewContent.linkClicked.connect(self.onLinkClicked)
        # 绑定信号槽
        Signals.showCoded.connect(self.renderCode)
        Signals.showReadmed.connect(self.renderReadme)
        Signals.urlLoaded.connect(self.onUrlLoaded)
        Signals.runExampled.connect(self._runFile)
        Signals.cloneFinished.connect(lambda: self._showNotice('更新例子完成'))
        Signals.cloneFinished.connect(self.treeViewCatalogs.initCatalog)
        Signals.cloneFinished.connect(self.renderReadme)
        Signals.progressStoped.connect(self.widgetCatalogs.stop)
        Signals.progressUpdated.connect(self.widgetCatalogs.setValue)
        Signals.updateDialogShowed.connect(self._initUpdate)

    def _initLanguage(self):
        """加载国际化翻译
        """
        if QLocale.system().language() in (QLocale.China, QLocale.Chinese, QLocale.Taiwan, QLocale.HongKong):
            # 加载中文
            translator = QTranslator(self)
            translator.load('Resources/pyqtclient_zh_CN.qm')
            QApplication.instance().installTranslator(translator)

    def _initWebView(self):
        """初始化网页"""
        # 右键菜单
        self._webviewMenu = QMenu(self.tr('Menu'), self.webViewContent)
        self._webviewactRun = QAction(
            self.tr('Run'), self._webviewMenu, triggered=self._doActRun)
        self._webviewactView = QAction(
            self.tr('View'), self._webviewMenu, triggered=self._doActView)
        self._webviewactFolder = QAction(
            self.tr('Open'), self._webviewMenu, triggered=self._doActOpen)
        self._webviewMenu.addAction(self._webviewactRun)
        self._webviewMenu.addAction(self._webviewactView)
        self._webviewMenu.addAction(self._webviewactFolder)

        self.webViewContent.customContextMenuRequested.connect(
            self._showWebMenu)
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

    def _doActRun(self):
        """右键菜单运行代码
        """
        path = self.sender().data()
        Signals.runExampled.emit(path)

    def _doActView(self):
        """右键菜单查看代码
        """
        path = self.sender().data()
        try:
            code = open(path, 'rb').read().decode(errors='ignore')
            Signals.showCoded.emit(code)
        except Exception as e:
            AppLog.warn(str(e))

    def _doActOpen(self):
        """右键菜单打开文件夹
        """
        path = self.sender().data()
        openFolder(path)

    def _showWebMenu(self, pos):
        """显示网页右键菜单
        :param pos:            点击位置
        """
        hit = self.webViewContent.page().currentFrame().hitTestContent(pos)
        url = hit.linkUrl()
        if url.isValid():
            path = url.toLocalFile().strip().replace('\\', '/')
            names = path.split('Markdown/')
            if len(names) == 1:
                return
            path = os.path.abspath(os.path.join(
                Constants.DirCurrent, names[1]))
            AppLog.debug('path: {}'.format(path))
            AppLog.debug('isdir: {}'.format(os.path.isdir(path)))
            self._webviewactRun.setData(path)
            self._webviewactView.setData(path)
            self._webviewactFolder.setData(path)
            if os.path.exists(path) and os.path.isdir(path):
                self._webviewactRun.setVisible(False)
                self._webviewactView.setVisible(False)
                self._webviewactFolder.setVisible(True)
            elif os.path.exists(path) and os.path.isfile(path):
                self._webviewactRun.setVisible(True)
                self._webviewactView.setVisible(True)
                self._webviewactFolder.setVisible(True)
            self._webviewMenu.exec_(QCursor.pos())

    def _showNotice(self, message, timeout=2000):
        """底部显示提示
        :param message:        提示消息
        """
        if hasattr(self, '_tip'):
            self._tip._hideTimer.stop()
            self._tip.close()
            self._tip.deleteLater()
            del self._tip
        self._tip = ToolTip()
        self._tip.setText(message)
        self._tip.show()
        self._tip.move(
            self.pos().x() + int((self.width() - self._tip.width()) / 2),
            self.pos().y() + self.height() - 60,
        )
        self._tip._hideTimer.timeout.connect(self._tip.close)
        self._tip._hideTimer.start(timeout)

    @pyqtSlot()
    def on_buttonSkin_clicked(self):
        """选择主题样式
        """
        if not hasattr(self, 'skinDialog'):
            self.skinDialog = SkinDialog(self)
        self.skinDialog.exec_()

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
        Signals.filterChanged.emit(text)

    @pyqtSlot()
    def on_buttonClear_clicked(self):
        """点击清空按钮
        """
        self.lineEditSearch.setText('')

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019年1月9日
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: Widgets.MainWindowBase
@description: 
"""

import os
import webbrowser

from PyQt5.QtCore import (QCoreApplication, QLocale, Qt, QTranslator, QUrl,
                          QVariant, pyqtSlot)
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QAction, QApplication, QMenu
from Utils import Constants
from Utils.CommonUtil import (AppLog, Setting, Signals, get_avatar_path,
                              openFolder)
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
        self.tips2233 = {}
        self.setupUi(self)
        # 隐藏还原按钮
        self.buttonNormal.setVisible(False)
        # 隐藏目录树的滑动条
        self.treeViewCatalogs.verticalScrollBar().setVisible(False)
        # 加载鼠标样式
        ThemeManager.loadCursor(self.widgetMain)
        ThemeManager.setPointerCursors([
            self.buttonHead,  # 主界面头像
            self.buttonClear,  # 主界面清空按钮
            self.buttonGithub,  # Github按钮
            self.buttonQQ,  # QQ按钮
            self.buttonGroup,  # 群按钮
            self.buttonBackToUp,  # 返回顶部按钮
            self.buttonHome  # 显示主页readme
        ])
        # 安装事件过滤器
        self._initEventFilter()
        # 初始化2233提示语
        self._init2233Tips()
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

    def _init2233Tips(self):
        """初始化2233提示语"""
        self.tips2233 = {
            self.buttonHead:
                QCoreApplication.translate('MainWindowBase', '登录才可以看到头像哦~'),
            self.lineEditSearch:
                QCoreApplication.translate('MainWindowBase', '找不到想要的？试试搜索吧！'),
            self.buttonGithub:
                QCoreApplication.translate('MainWindowBase', 'GayHub！求关注喵！'),
            self.buttonQQ:
                QCoreApplication.translate('MainWindowBase', '这是我的QQ~，还是加群吧！'),
            self.buttonGroup:
                QCoreApplication.translate('MainWindowBase', '加入PY交流！我是新手！'),
            self.buttonHome:
                QCoreApplication.translate('MainWindowBase', '点它就可以回到首页啦！'),
            self.buttonBackToUp:
                QCoreApplication.translate('MainWindowBase', '要回到开始的地方么？'),
            self.buttonSkin:
                QCoreApplication.translate('MainWindowBase', '要更换biu特佛的主题么？'),
            self.buttonIssues:
                QCoreApplication.translate('MainWindowBase', '要说点什么吗？'),
            self.buttonMinimum:
                QCoreApplication.translate('MainWindowBase', '点我可以最小化哦！'),
            self.buttonMaximum:
                QCoreApplication.translate('MainWindowBase', '点我可以最大化哦！'),
            self.buttonNormal:
                QCoreApplication.translate('MainWindowBase', '点我可以还原哦！'),
            self.buttonClose:
                QCoreApplication.translate('MainWindowBase', '点我就拜拜啦！'),
        }

    def _initEventFilter(self):
        """安装事件过滤器"""
        self.widgetMain.installEventFilter(self)
        self.buttonHead.installEventFilter(self)
        self.lineEditSearch.installEventFilter(self)
        self.buttonGithub.installEventFilter(self)
        self.buttonQQ.installEventFilter(self)
        self.buttonGroup.installEventFilter(self)
        self.buttonHome.installEventFilter(self)
        self.buttonBackToUp.installEventFilter(self)
        self.buttonSkin.installEventFilter(self)
        self.buttonIssues.installEventFilter(self)
        self.buttonMinimum.installEventFilter(self)
        self.buttonMaximum.installEventFilter(self)
        self.buttonNormal.installEventFilter(self)
        self.buttonClose.installEventFilter(self)

    def _initSignals(self):
        """初始化信号槽"""
        self.webViewContent.loadFinished.connect(self._exposeInterface)
        self.webViewContent.linkClicked.connect(self.onLinkClicked)
        # 绑定信号槽
        Signals.showCoded.connect(self.renderCode)
        Signals.showReadmed.connect(self.renderReadme)
        Signals.urlLoaded.connect(self.onUrlLoaded)
        Signals.anchorJumped.connect(self.onAnchorJumped)
        Signals.runExampled.connect(self._runFile)
        Signals.runUiFile.connect(self._runUiFile)
        Signals.cloneFinished.connect(lambda: self._showNotice(
            QCoreApplication.translate('MainWindowBase',
                                       'Update Example Finished')))
        Signals.cloneFinished.connect(self.treeViewCatalogs.initCatalog)
        Signals.cloneFinished.connect(self.renderReadme)
        Signals.progressStoped.connect(self.widgetCatalogs.stop)
        Signals.progressUpdated.connect(self.widgetCatalogs.setValue)
        Signals.updateDialogShowed.connect(self._initUpdate)
        Signals.showDonate.connect(self._initDonate)

    def _initLanguage(self):
        """加载国际化翻译
        """
        if QLocale.system().language() in (QLocale.China, QLocale.Chinese,
                                           QLocale.Taiwan, QLocale.HongKong):
            # 加载中文
            translator = QTranslator(self)
            translator.load('Resources/pyqtclient_zh_CN.qm')
            QApplication.instance().installTranslator(translator)
            AppLog.info('install local language')

    def _initUser(self):
        """初始化用户信息"""
        account = Setting.value('account', '', str)
        if not account:
            return
        accounts = Setting.value('accounts', {}, QVariant)
        path = get_avatar_path(account)
        if os.path.exists(path):
            Constants.ImageAvatar = path
        if account in accounts and not Constants.ImageAvatar.endswith(
                'avatar.png'):
            Constants._Account, Constants._Status, Constants._Emoji = accounts[
                account]
            Constants._Username = account
        self._setHeadImage()

    def _initWebView(self):
        """初始化网页"""
        # 右键菜单
        self._webviewMenu = QMenu(
            QCoreApplication.translate('MainWindowBase', 'Menu'),
            self.webViewContent)
        self._webviewactRun = QAction(QCoreApplication.translate(
            'MainWindowBase', 'Run'),
                                      self._webviewMenu,
                                      triggered=self._doActRun)
        self._webviewactView = QAction(QCoreApplication.translate(
            'MainWindowBase', 'View'),
                                       self._webviewMenu,
                                       triggered=self._doActView)
        self._webviewactFolder = QAction(QCoreApplication.translate(
            'MainWindowBase', 'Open'),
                                         self._webviewMenu,
                                         triggered=self._doActOpen)
        self._webviewMenu.addAction(self._webviewactRun)
        self._webviewMenu.addAction(self._webviewactView)
        self._webviewMenu.addAction(self._webviewactFolder)

        if 'DEBUG_MENU' in os.environ:
            self._webviewMenu.addAction(
                self.webViewContent.pageAction(QWebPage.InspectElement))
        self.webViewContent.customContextMenuRequested.connect(
            self._showWebMenu)
        settings = QWebSettings.globalSettings()
        # 设置默认编码
        settings.setDefaultTextEncoding('UTF-8')
        # 设置缓存路径
        settings.setLocalStoragePath('Resources/Cache')
        settings.setOfflineStoragePath('Resources/Cache')
        settings.setOfflineWebApplicationCachePath('Resources/Cache')
        # 开启开发人员工具
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        settings.setAttribute(QWebSettings.PluginsEnabled, True)
        settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebSettings.JavascriptCanCloseWindows, True)
        settings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebSettings.OfflineStorageDatabaseEnabled, True)
        settings.setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled,
                              True)
        settings.setAttribute(QWebSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls,
                              True)
        settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebSettings.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebSettings.WebSecurityEnabled, True)
        if hasattr(settings, 'ErrorPageEnabled'):
            settings.setAttribute(QWebSettings.ErrorPageEnabled, False)

        page = self.webViewContent.page()
        # 设置链接可以点击
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        # 使用自定义的网络请求类(方便处理一些链接点击)
        page.setNetworkAccessManager(NetworkAccessManager(self.webViewContent))

        # 加载readme
        self.webViewContent.load(
            QUrl.fromLocalFile(os.path.abspath(Constants.HomeFile)))

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
            path = os.path.abspath(os.path.join(Constants.DirCurrent, names[1]))
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
        else:
            if 'DEBUG_MENU' in os.environ:
                self._webviewactRun.setVisible(False)
                self._webviewactView.setVisible(False)
                self._webviewactFolder.setVisible(False)
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

    def _setHeadImage(self):
        """设置头像"""
        self.buttonHead.image = Constants.ImageAvatar
        tip = Constants._Username
        if Constants._Status or Constants._Emoji:
            tip += ': {} {}'.format(Constants._Emoji, Constants._Status)
        self.buttonHead.setToolTip(tip)

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

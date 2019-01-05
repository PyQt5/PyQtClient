#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月4日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Utils.Application
@description: 
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2019 Irony"
__Version__ = "Version 1.0"


class QSingleApplication(QApplication):

    messageReceived = pyqtSignal(str)

    def __init__(self, name, *args, **kwargs):
        super(QSingleApplication, self).__init__(*args, **kwargs)
        self._socketName = name
        self._activationWindow = None
        self._socketServer = None
        self._socketIn = None
        self._socketOut = None
        self._running = False

        # 先尝试连接
        self._socketOut = QLocalSocket(self)
        self._socketOut.connectToServer(self._socketName)
        self._socketOut.error.connect(self.handleError)
        self._running = self._socketOut.waitForConnected()

        if not self._running:  # 程序未运行
            self._socketOut.close()
            del self._socketOut
            # 创建本地server
            self._socketServer = QLocalServer(self)
            self._socketServer.listen(self._socketName)
            self._socketServer.newConnection.connect(self._onNewConnection)
            self.aboutToQuit.connect(self.removeServer)

    def handleError(self, message):
        print("handleError message: ", message)

    def isRunning(self):
        return self._running

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(self, activationWindow):
        # 设置需要激活的窗口
        self._activationWindow = activationWindow

    def activateWindow(self):
        try:
            self._activationWindow.setWindowState(
                self._activationWindow.windowState() & ~Qt.WindowMinimized)
#             self._activationWindow.raise_()
            self._activationWindow.showNormal()
            self._activationWindow.activateWindow()
        except Exception as e:
            print(e)

    def sendMessage(self, message, msecs=5000):
        if not self._socketOut:
            return False
        if not isinstance(message, bytes):
            message = str(message).encode()
        self._socketOut.write(message)
        if not self._socketOut.waitForBytesWritten(msecs):
            raise Exception("Bytes not written within %ss" %
                            (msecs / 1000.))
        return True

    def _onNewConnection(self):
        if self._socketIn:
            self._socketIn.readyRead.disconnect(self._onReadyRead)
        self._socketIn = self._socketServer.nextPendingConnection()
        if not self._socketIn:
            return
        self._socketIn.readyRead.connect(self._onReadyRead)

    def _onReadyRead(self):
        while 1:
            message = self._socketIn.readLine()
            if not message:
                break
            if message == b'show':
                self.activateWindow()
            self.messageReceived.emit(message.data().decode())

    def removeServer(self):
        self._socketServer.close()
        self._socketServer.removeServer(self._socketName)

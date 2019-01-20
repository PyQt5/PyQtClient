#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年1月18日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: Dialogs.ErrorDialog
@description: 
"""
import os
import re
import sys

from PyQt5.QtCore import Qt, pyqtSlot, QProcess

from Dialogs.MoveDialog import MoveDialog
from UiFiles.Ui_ErrorDialog import Ui_FormErrorDialog
from Utils.ThemeManager import ThemeManager


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"


class ErrorDialog(MoveDialog, Ui_FormErrorDialog):

    def __init__(self, message, *args, reqfile='', **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)
        self.reqfile = reqfile
        self.setupUi(self)
        # 关闭后自动销毁
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 加载鼠标样式
        ThemeManager.loadCursor(self)
        self.plainTextEditDetail.appendPlainText(message)

    @pyqtSlot()
    def on_buttonInstall_clicked(self):
        """通过pip安装依赖
        """
        self.widgetErrorBg.setCurrentIndex(1)
        if self.reqfile and os.path.isfile(self.reqfile):
            with open(self.reqfile, 'rb') as fp:
                modules = fp.read().decode().replace('\r\n', ' ').replace('\n', ' ')
                self.lineEditPip.setText(''.join(modules))
                if modules:
                    self.lineEditPip.returnPressed.emit()
        else:
            modules = re.findall("No module named '(.*?)'",
                                 self.plainTextEditDetail.toPlainText())
            if not modules:
                return
            modules = [m.split('.')[0] for m in modules]
            self.lineEditPip.setText(''.join(modules))
            self.lineEditPip.returnPressed.emit()

    def on_lineEditPip_returnPressed(self):
        """按下回车键执行
        """
        text = self.lineEditPip.text().strip()
        if not text:
            return
        process = QProcess(self)
        process.readyReadStandardError.connect(self.onReadyReadStandardError)
        process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        process.start(sys.executable, [
                      '-m', 'pip', 'install'] + text.split(' '))

    def onReadyReadStandardError(self):
        result = self.sender().readAllStandardError().data().decode()
        self.plainTextEditPip.appendPlainText(result)

    def onReadyReadStandardOutput(self):
        result = self.sender().readAllStandardOutput().data().decode()
        self.plainTextEditPip.appendPlainText(result)


if __name__ == '__main__':
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ErrorDialog('')
    w.show()
    sys.exit(app.exec_())

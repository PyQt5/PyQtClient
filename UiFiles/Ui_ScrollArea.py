# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Workspace\PyQtClient\UiFiles\ScrollArea.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormScrollArea(object):
    def setupUi(self, FormScrollArea):
        FormScrollArea.setObjectName("FormScrollArea")
        FormScrollArea.resize(900, 612)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FormScrollArea)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(FormScrollArea)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 900, 612))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setContentsMargins(30, 26, 30, 26)
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(26)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.retranslateUi(FormScrollArea)
        QtCore.QMetaObject.connectSlotsByName(FormScrollArea)

    def retranslateUi(self, FormScrollArea):
        _translate = QtCore.QCoreApplication.translate
        FormScrollArea.setWindowTitle(_translate("FormScrollArea", "ScrollArea"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormScrollArea = QtWidgets.QWidget()
    ui = Ui_FormScrollArea()
    ui.setupUi(FormScrollArea)
    FormScrollArea.show()
    sys.exit(app.exec_())


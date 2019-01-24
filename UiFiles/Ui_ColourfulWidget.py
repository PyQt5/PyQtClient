# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Workspace\PyQtClient\UiFiles\ColourfulWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormColourful(object):
    def setupUi(self, FormColourful):
        FormColourful.setObjectName("FormColourful")
        FormColourful.resize(900, 612)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FormColourful)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(FormColourful)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 898, 610))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setContentsMargins(30, 26, 30, 26)
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(26)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.retranslateUi(FormColourful)
        QtCore.QMetaObject.connectSlotsByName(FormColourful)

    def retranslateUi(self, FormColourful):
        _translate = QtCore.QCoreApplication.translate
        FormColourful.setWindowTitle(_translate("FormColourful", "Colourful"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormColourful = QtWidgets.QWidget()
    ui = Ui_FormColourful()
    ui.setupUi(FormColourful)
    FormColourful.show()
    sys.exit(app.exec_())


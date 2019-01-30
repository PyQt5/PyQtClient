# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Workspace\PyQtClient\UiFiles\PreviewWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormPreviewWidget(object):
    def setupUi(self, FormPreviewWidget):
        FormPreviewWidget.setObjectName("FormPreviewWidget")
        FormPreviewWidget.resize(636, 570)
        self.gridLayout = QtWidgets.QGridLayout(FormPreviewWidget)
        self.gridLayout.setVerticalSpacing(18)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.buttonPreviewPrevious = QtWidgets.QPushButton(FormPreviewWidget)
        self.buttonPreviewPrevious.setText("")
        self.buttonPreviewPrevious.setObjectName("buttonPreviewPrevious")
        self.gridLayout.addWidget(self.buttonPreviewPrevious, 1, 0, 1, 1)
        self.labelPreviewTitle = QtWidgets.QLabel(FormPreviewWidget)
        self.labelPreviewTitle.setText("")
        self.labelPreviewTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPreviewTitle.setObjectName("labelPreviewTitle")
        self.gridLayout.addWidget(self.labelPreviewTitle, 2, 2, 1, 1)
        self.labelPreviewImage = QtWidgets.QLabel(FormPreviewWidget)
        self.labelPreviewImage.setMinimumSize(QtCore.QSize(400, 385))
        self.labelPreviewImage.setText("")
        self.labelPreviewImage.setScaledContents(True)
        self.labelPreviewImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPreviewImage.setObjectName("labelPreviewImage")
        self.gridLayout.addWidget(self.labelPreviewImage, 1, 2, 1, 1)
        self.buttonPreviewNext = QtWidgets.QPushButton(FormPreviewWidget)
        self.buttonPreviewNext.setText("")
        self.buttonPreviewNext.setObjectName("buttonPreviewNext")
        self.gridLayout.addWidget(self.buttonPreviewNext, 1, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 3, 1, 1)
        self.widget_2 = QtWidgets.QWidget(FormPreviewWidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(-1, 8, -1, 15)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.buttonPreviewClose = QtWidgets.QPushButton(self.widget_2)
        self.buttonPreviewClose.setText("")
        self.buttonPreviewClose.setObjectName("buttonPreviewClose")
        self.horizontalLayout_2.addWidget(self.buttonPreviewClose)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.gridLayout.addWidget(self.widget_2, 4, 2, 1, 1)
        self.widget = QtWidgets.QWidget(FormPreviewWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.buttonPreviewApply = QtWidgets.QPushButton(self.widget)
        self.buttonPreviewApply.setObjectName("buttonPreviewApply")
        self.horizontalLayout.addWidget(self.buttonPreviewApply)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.gridLayout.addWidget(self.widget, 3, 2, 1, 1)

        self.retranslateUi(FormPreviewWidget)
        QtCore.QMetaObject.connectSlotsByName(FormPreviewWidget)

    def retranslateUi(self, FormPreviewWidget):
        _translate = QtCore.QCoreApplication.translate
        FormPreviewWidget.setWindowTitle(_translate("FormPreviewWidget", "Preview"))
        self.buttonPreviewApply.setText(_translate("FormPreviewWidget", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormPreviewWidget = QtWidgets.QWidget()
    ui = Ui_FormPreviewWidget()
    ui.setupUi(FormPreviewWidget)
    FormPreviewWidget.show()
    sys.exit(app.exec_())


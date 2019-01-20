# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Workspace\PyQtClient\UiFiles\DonateDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormDonateDialog(object):
    def setupUi(self, FormDonateDialog):
        FormDonateDialog.setObjectName("FormDonateDialog")
        FormDonateDialog.resize(641, 385)
        self.verticalLayout = QtWidgets.QVBoxLayout(FormDonateDialog)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetDonate = QtWidgets.QWidget(FormDonateDialog)
        self.widgetDonate.setProperty("active", True)
        self.widgetDonate.setObjectName("widgetDonate")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widgetDonate)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dialogTitlebar = QtWidgets.QWidget(self.widgetDonate)
        self.dialogTitlebar.setObjectName("dialogTitlebar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dialogTitlebar)
        self.horizontalLayout.setContentsMargins(0, 1, 1, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelTitle = QtWidgets.QLabel(self.dialogTitlebar)
        self.labelTitle.setIndent(6)
        self.labelTitle.setObjectName("labelTitle")
        self.horizontalLayout.addWidget(self.labelTitle)
        spacerItem = QtWidgets.QSpacerItem(260, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonClose = QtWidgets.QPushButton(self.dialogTitlebar)
        self.buttonClose.setText("")
        self.buttonClose.setAutoDefault(False)
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout_2.addWidget(self.dialogTitlebar)
        self.widgetImage = QtWidgets.QWidget(self.widgetDonate)
        self.widgetImage.setObjectName("widgetImage")
        self.gridLayout = QtWidgets.QGridLayout(self.widgetImage)
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.gridLayout.setObjectName("gridLayout")
        self.labelWechatImg = QtWidgets.QLabel(self.widgetImage)
        self.labelWechatImg.setMinimumSize(QtCore.QSize(300, 300))
        self.labelWechatImg.setMaximumSize(QtCore.QSize(300, 300))
        self.labelWechatImg.setText("")
        self.labelWechatImg.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWechatImg.setObjectName("labelWechatImg")
        self.gridLayout.addWidget(self.labelWechatImg, 0, 1, 1, 1)
        self.labelAlipayImg = QtWidgets.QLabel(self.widgetImage)
        self.labelAlipayImg.setMinimumSize(QtCore.QSize(300, 300))
        self.labelAlipayImg.setMaximumSize(QtCore.QSize(300, 300))
        self.labelAlipayImg.setText("")
        self.labelAlipayImg.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAlipayImg.setObjectName("labelAlipayImg")
        self.gridLayout.addWidget(self.labelAlipayImg, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widgetImage)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widgetImage)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.widgetImage)
        self.verticalLayout.addWidget(self.widgetDonate)

        self.retranslateUi(FormDonateDialog)
        self.buttonClose.clicked.connect(FormDonateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FormDonateDialog)

    def retranslateUi(self, FormDonateDialog):
        _translate = QtCore.QCoreApplication.translate
        FormDonateDialog.setWindowTitle(_translate("FormDonateDialog", "Donate"))
        self.labelTitle.setText(_translate("FormDonateDialog", "Donate"))
        self.label.setText(_translate("FormDonateDialog", "Alipay"))
        self.label_2.setText(_translate("FormDonateDialog", "Wechat"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormDonateDialog = QtWidgets.QDialog()
    ui = Ui_FormDonateDialog()
    ui.setupUi(FormDonateDialog)
    FormDonateDialog.show()
    sys.exit(app.exec_())


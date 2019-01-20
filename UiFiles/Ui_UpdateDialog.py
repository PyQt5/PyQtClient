# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Workspace\PyQtClient\UiFiles\UpdateDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormUpdateDialog(object):
    def setupUi(self, FormUpdateDialog):
        FormUpdateDialog.setObjectName("FormUpdateDialog")
        FormUpdateDialog.resize(600, 448)
        self.verticalLayout = QtWidgets.QVBoxLayout(FormUpdateDialog)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetUpdate = QtWidgets.QWidget(FormUpdateDialog)
        self.widgetUpdate.setProperty("active", True)
        self.widgetUpdate.setObjectName("widgetUpdate")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widgetUpdate)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dialogTitlebar = QtWidgets.QWidget(self.widgetUpdate)
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
        self.widgetUpdateBg = QtWidgets.QWidget(self.widgetUpdate)
        self.widgetUpdateBg.setObjectName("widgetUpdateBg")
        self.gridLayout = QtWidgets.QGridLayout(self.widgetUpdateBg)
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBarUpdate = QtWidgets.QProgressBar(self.widgetUpdateBg)
        self.progressBarUpdate.setMinimumSize(QtCore.QSize(0, 40))
        self.progressBarUpdate.setProperty("value", 0)
        self.progressBarUpdate.setTextVisible(False)
        self.progressBarUpdate.setObjectName("progressBarUpdate")
        self.gridLayout.addWidget(self.progressBarUpdate, 2, 0, 1, 2)
        self.labelMessage = QtWidgets.QLabel(self.widgetUpdateBg)
        self.labelMessage.setText("")
        self.labelMessage.setObjectName("labelMessage")
        self.gridLayout.addWidget(self.labelMessage, 1, 0, 1, 2)
        self.plainTextEditDetail = QtWidgets.QPlainTextEdit(self.widgetUpdateBg)
        self.plainTextEditDetail.setMinimumSize(QtCore.QSize(0, 250))
        self.plainTextEditDetail.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plainTextEditDetail.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEditDetail.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEditDetail.setUndoRedoEnabled(False)
        self.plainTextEditDetail.setReadOnly(True)
        self.plainTextEditDetail.setObjectName("plainTextEditDetail")
        self.gridLayout.addWidget(self.plainTextEditDetail, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widgetUpdateBg)
        self.verticalLayout.addWidget(self.widgetUpdate)

        self.retranslateUi(FormUpdateDialog)
        self.buttonClose.clicked.connect(FormUpdateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FormUpdateDialog)

    def retranslateUi(self, FormUpdateDialog):
        _translate = QtCore.QCoreApplication.translate
        FormUpdateDialog.setWindowTitle(_translate("FormUpdateDialog", "Update"))
        self.labelTitle.setText(_translate("FormUpdateDialog", "Update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormUpdateDialog = QtWidgets.QDialog()
    ui = Ui_FormUpdateDialog()
    ui.setupUi(FormUpdateDialog)
    FormUpdateDialog.show()
    sys.exit(app.exec_())


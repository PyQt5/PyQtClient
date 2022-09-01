# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Workspace\PyQtClient\UiFiles\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormMainWindow(object):
    def setupUi(self, FormMainWindow):
        FormMainWindow.setObjectName("FormMainWindow")
        FormMainWindow.resize(800, 600)
        FormMainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayout = QtWidgets.QVBoxLayout(FormMainWindow)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetMain = QtWidgets.QWidget(FormMainWindow)
        self.widgetMain.setObjectName("widgetMain")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widgetMain)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widgetTitlebar = QtWidgets.QWidget(self.widgetMain)
        self.widgetTitlebar.setObjectName("widgetTitlebar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetTitlebar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(369, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonSkin = QtWidgets.QPushButton(self.widgetTitlebar)
        self.buttonSkin.setText("")
        self.buttonSkin.setObjectName("buttonSkin")
        self.horizontalLayout.addWidget(self.buttonSkin)
        self.buttonIssues = QtWidgets.QPushButton(self.widgetTitlebar)
        self.buttonIssues.setText("")
        self.buttonIssues.setObjectName("buttonIssues")
        self.horizontalLayout.addWidget(self.buttonIssues)
        self.buttonMinimum = QtWidgets.QPushButton(self.widgetTitlebar)
        self.buttonMinimum.setText("")
        self.buttonMinimum.setObjectName("buttonMinimum")
        self.horizontalLayout.addWidget(self.buttonMinimum)
        self.buttonMaximum = QtWidgets.QPushButton(self.widgetTitlebar)
        self.buttonMaximum.setText("")
        self.buttonMaximum.setObjectName("buttonMaximum")
        self.horizontalLayout.addWidget(self.buttonMaximum)
        self.buttonNormal = QtWidgets.QPushButton(self.widgetTitlebar)
        self.buttonNormal.setText("")
        self.buttonNormal.setObjectName("buttonNormal")
        self.horizontalLayout.addWidget(self.buttonNormal)
        self.buttonClose = QtWidgets.QPushButton(self.widgetTitlebar)
        self.buttonClose.setText("")
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout.addWidget(self.buttonClose)
        self.verticalLayout_2.addWidget(self.widgetTitlebar)
        self.widgetCentral = QtWidgets.QWidget(self.widgetMain)
        self.widgetCentral.setObjectName("widgetCentral")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widgetCentral)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widgetCatalogs = WaterWidget(self.widgetCentral)
        self.widgetCatalogs.setObjectName("widgetCatalogs")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widgetCatalogs)
        self.verticalLayout_4.setContentsMargins(20, 30, 20, 30)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widgetHead = QtWidgets.QWidget(self.widgetCatalogs)
        self.widgetHead.setObjectName("widgetHead")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widgetHead)
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.buttonHead = RotateButton(self.widgetHead)
        self.buttonHead.setText("")
        self.buttonHead.setObjectName("buttonHead")
        self.horizontalLayout_4.addWidget(self.buttonHead)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_4.addWidget(self.widgetHead)
        self.widgetSearch = QtWidgets.QWidget(self.widgetCatalogs)
        self.widgetSearch.setObjectName("widgetSearch")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetSearch)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEditSearch = QtWidgets.QLineEdit(self.widgetSearch)
        self.lineEditSearch.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEditSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.horizontalLayout_3.addWidget(self.lineEditSearch)
        self.buttonClear = RubberBandButton(self.widgetSearch)
        self.buttonClear.setText("")
        self.buttonClear.setObjectName("buttonClear")
        self.horizontalLayout_3.addWidget(self.buttonClear)
        self.verticalLayout_4.addWidget(self.widgetSearch)
        self.treeViewCatalogs = TreeView(self.widgetCatalogs)
        self.treeViewCatalogs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewCatalogs.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.treeViewCatalogs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeViewCatalogs.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeViewCatalogs.setAnimated(True)
        self.treeViewCatalogs.setHeaderHidden(True)
        self.treeViewCatalogs.setExpandsOnDoubleClick(False)
        self.treeViewCatalogs.setObjectName("treeViewCatalogs")
        self.verticalLayout_4.addWidget(self.treeViewCatalogs)
        self.horizontalLayout_2.addWidget(self.widgetCatalogs)
        self.widgetTools = QtWidgets.QWidget(self.widgetCentral)
        self.widgetTools.setObjectName("widgetTools")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widgetTools)
        self.verticalLayout_5.setContentsMargins(12, 35, 12, 30)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.buttonGithub = RotateButton(self.widgetTools)
        self.buttonGithub.setText("")
        self.buttonGithub.setObjectName("buttonGithub")
        self.verticalLayout_5.addWidget(self.buttonGithub)
        self.buttonQQ = RotateButton(self.widgetTools)
        self.buttonQQ.setText("")
        self.buttonQQ.setObjectName("buttonQQ")
        self.verticalLayout_5.addWidget(self.buttonQQ)
        self.buttonGroup = RotateButton(self.widgetTools)
        self.buttonGroup.setText("")
        self.buttonGroup.setObjectName("buttonGroup")
        self.verticalLayout_5.addWidget(self.buttonGroup)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.buttonHome = RubberBandButton(self.widgetTools)
        self.buttonHome.setText("")
        self.buttonHome.setObjectName("buttonHome")
        self.verticalLayout_5.addWidget(self.buttonHome)
        self.buttonBackToUp = RubberBandButton(self.widgetTools)
        self.buttonBackToUp.setText("")
        self.buttonBackToUp.setObjectName("buttonBackToUp")
        self.verticalLayout_5.addWidget(self.buttonBackToUp)
        self.horizontalLayout_2.addWidget(self.widgetTools)
        self.widgetContents = QtWidgets.QWidget(self.widgetCentral)
        self.widgetContents.setObjectName("widgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widgetContents)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.webViewContent = QtWebKitWidgets.QWebView(self.widgetContents)
        self.webViewContent.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.webViewContent.setProperty("url", QtCore.QUrl("about:blank"))
        self.webViewContent.setObjectName("webViewContent")
        self.verticalLayout_3.addWidget(self.webViewContent)
        self.horizontalLayout_2.addWidget(self.widgetContents)
        self.verticalLayout_2.addWidget(self.widgetCentral)
        self.verticalLayout.addWidget(self.widgetMain)

        self.retranslateUi(FormMainWindow)
        QtCore.QMetaObject.connectSlotsByName(FormMainWindow)

    def retranslateUi(self, FormMainWindow):
        _translate = QtCore.QCoreApplication.translate
        FormMainWindow.setWindowTitle(_translate("FormMainWindow", "PyQtClient"))
        self.buttonGithub.setToolTip(_translate("FormMainWindow", "Project Url"))
        self.buttonQQ.setToolTip(_translate("FormMainWindow", "QQ Chat"))
        self.buttonGroup.setToolTip(_translate("FormMainWindow", "QQ Group"))
        self.buttonHome.setToolTip(_translate("FormMainWindow", "Home Page"))
        self.buttonBackToUp.setToolTip(_translate("FormMainWindow", "Back to Top"))
from PyQt5 import QtWebKitWidgets
from Widgets.Buttons.RotateButton import RotateButton
from Widgets.Buttons.RubberBandButton import RubberBandButton
from Widgets.TreeView import TreeView
from Widgets.WaterWidget import WaterWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormMainWindow = QtWidgets.QWidget()
    ui = Ui_FormMainWindow()
    ui.setupUi(FormMainWindow)
    FormMainWindow.show()
    sys.exit(app.exec_())

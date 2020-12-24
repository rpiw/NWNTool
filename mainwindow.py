# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(631, 521)
        self.actionOpen_Database = QAction(MainWindow)
        self.actionOpen_Database.setObjectName(u"actionOpen_Database")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionConfigure = QAction(MainWindow)
        self.actionConfigure.setObjectName(u"actionConfigure")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSearch = QAction(MainWindow)
        self.actionSearch.setObjectName(u"actionSearch")
        self.actionSearch_2 = QAction(MainWindow)
        self.actionSearch_2.setObjectName(u"actionSearch_2")
        self.actionSubscriptions = QAction(MainWindow)
        self.actionSubscriptions.setObjectName(u"actionSubscriptions")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 8, 611, 471))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 6, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 3, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 4, 2, 1, 1)

        self.lineEdit_1 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_1.setObjectName(u"lineEdit_1")

        self.gridLayout.addWidget(self.lineEdit_1, 2, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout.addWidget(self.lineEdit_3, 4, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 5, 2, 1, 1)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.label_1 = QLabel(self.verticalLayoutWidget)
        self.label_1.setObjectName(u"label_1")

        self.gridLayout.addWidget(self.label_1, 2, 0, 1, 1)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)

        self.lineEdit_5 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout.addWidget(self.lineEdit_5, 6, 1, 1, 1)

        self.pushButton_1 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_1.setObjectName(u"pushButton_1")

        self.gridLayout.addWidget(self.pushButton_1, 2, 2, 1, 1)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout.addWidget(self.lineEdit_4, 5, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tableView = QTableView(self.verticalLayoutWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 631, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuModules = QMenu(self.menubar)
        self.menuModules.setObjectName(u"menuModules")
        self.menuVault = QMenu(self.menubar)
        self.menuVault.setObjectName(u"menuVault")
        self.menuSteam_Workshop = QMenu(self.menubar)
        self.menuSteam_Workshop.setObjectName(u"menuSteam_Workshop")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label_4.setBuddy(self.lineEdit_4)
        self.label_5.setBuddy(self.lineEdit_5)
        self.label_1.setBuddy(self.lineEdit_1)
        self.label_3.setBuddy(self.lineEdit_3)
        self.label_2.setBuddy(self.lineEdit_2)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEdit_1, self.pushButton_1)
        QWidget.setTabOrder(self.pushButton_1, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.pushButton_4)
        QWidget.setTabOrder(self.pushButton_4, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.pushButton_5)
        QWidget.setTabOrder(self.pushButton_5, self.tableView)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuModules.menuAction())
        self.menubar.addAction(self.menuVault.menuAction())
        self.menubar.addAction(self.menuSteam_Workshop.menuAction())
        self.menuFile.addAction(self.actionOpen_Database)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionConfigure)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuVault.addAction(self.actionSearch)
        self.menuSteam_Workshop.addAction(self.actionSearch_2)
        self.menuSteam_Workshop.addAction(self.actionSubscriptions)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_Database.setText(QCoreApplication.translate("MainWindow", u"Open Database", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.actionConfigure.setText(QCoreApplication.translate("MainWindow", u"Configure", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.actionSearch_2.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.actionSubscriptions.setText(QCoreApplication.translate("MainWindow", u"Subscriptions", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"EE local directory", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Set directory", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Set directory", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Set directory", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"NWNTool directory", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"Diamond Edition", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Enhanced Edition", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Set directory", None))
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow", u"Set directory", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"DE local directory", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuModules.setTitle(QCoreApplication.translate("MainWindow", u"Modules", None))
        self.menuVault.setTitle(QCoreApplication.translate("MainWindow", u"Vault", None))
        self.menuSteam_Workshop.setTitle(QCoreApplication.translate("MainWindow", u"Steam Workshop", None))
    # retranslateUi


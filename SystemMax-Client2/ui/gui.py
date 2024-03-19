# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1434, 829)
        MainWindow.setStyleSheet(u"background-color: #122839;")
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName(u"actionLogout")
        self.actionView = QAction(MainWindow)
        self.actionView.setObjectName(u"actionView")
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName(u"actionStop")
        self.actionAdd_Terminal = QAction(MainWindow)
        self.actionAdd_Terminal.setObjectName(u"actionAdd_Terminal")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 20, 521, 51))
        self.label.setStyleSheet(u"font: 24pt \"Fira Code\";\n"
"background-color: #070F2B;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    min-width: 10em;\n"
"    padding: 6px;")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 90, 951, 681))
        self.terminalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.terminalLayout.setObjectName(u"terminalLayout")
        self.terminalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(980, 100, 391, 681))
        self.chatLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.chatLayout.setObjectName(u"chatLayout")
        self.chatLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(990, 20, 371, 51))
        self.label_2.setStyleSheet(u"font: 24pt \"Fira Code\";\n"
"background-color: #070F2B;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    min-width: 10em;\n"
"    padding: 6px;")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QRect(0, 0, 1434, 37))
        self.menuLogout = QMenu(self.menuBar)
        self.menuLogout.setObjectName(u"menuLogout")
        self.menuProfile = QMenu(self.menuBar)
        self.menuProfile.setObjectName(u"menuProfile")
        self.menuProcess = QMenu(self.menuBar)
        self.menuProcess.setObjectName(u"menuProcess")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuLogout.menuAction())
        self.menuBar.addAction(self.menuProfile.menuAction())
        self.menuBar.addAction(self.menuProcess.menuAction())
        self.menuLogout.addAction(self.actionAdd_Terminal)
        self.menuLogout.addAction(self.actionLogout)
        self.menuProfile.addAction(self.actionView)
        self.menuProcess.addAction(self.actionStop)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLogout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.actionView.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.actionStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.actionAdd_Terminal.setText(QCoreApplication.translate("MainWindow", u"Add Terminal", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Native OS terminal - SystemMax CP", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Chat with out Assistent", None))
        self.menuLogout.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuProfile.setTitle(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.menuProcess.setTitle(QCoreApplication.translate("MainWindow", u"Process", None))
    # retranslateUi


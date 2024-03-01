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
        MainWindow.resize(1400, 788)
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName(u"actionLogout")
        self.actionView = QAction(MainWindow)
        self.actionView.setObjectName(u"actionView")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(190, 10, 651, 30))
        self.label.setStyleSheet(u"font-size:30px")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 50, 911, 641))
        self.terminalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.terminalLayout.setObjectName(u"terminalLayout")
        self.terminalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(980, 50, 391, 641))
        self.chatLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.chatLayout.setObjectName(u"chatLayout")
        self.chatLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(1000, 10, 651, 30))
        self.label_2.setStyleSheet(u"font-size:30px")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QRect(0, 0, 1400, 37))
        self.menuLogout = QMenu(self.menuBar)
        self.menuLogout.setObjectName(u"menuLogout")
        self.menuProfile = QMenu(self.menuBar)
        self.menuProfile.setObjectName(u"menuProfile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuLogout.menuAction())
        self.menuBar.addAction(self.menuProfile.menuAction())
        self.menuLogout.addAction(self.actionLogout)
        self.menuProfile.addAction(self.actionView)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLogout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.actionView.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Native OS terminal - SystemMax CP", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Chat with out Assistent", None))
        self.menuLogout.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuProfile.setTitle(QCoreApplication.translate("MainWindow", u"Profile", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setGeometry(QRect(210, 130, 100, 32))
        self.goToRegisterButton = QPushButton(self.centralwidget)
        self.goToRegisterButton.setObjectName(u"goToRegisterButton")
        self.goToRegisterButton.setGeometry(QRect(370, 130, 100, 32))
        self.emailLineEdit = QLineEdit(self.centralwidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")
        self.emailLineEdit.setGeometry(QRect(210, 60, 261, 21))
        self.passwordLineEdit = QLineEdit(self.centralwidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setGeometry(QRect(210, 90, 261, 21))
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(230, 20, 231, 20))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(150, 60, 58, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(150, 90, 58, 16))
        self.serverStatusLabel = QLabel(self.centralwidget)
        self.serverStatusLabel.setObjectName(u"serverStatusLabel")
        self.serverStatusLabel.setGeometry(QRect(250, 180, 171, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 37))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.goToRegisterButton.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Welcome to SystemMax! Please Login", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"email:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"password:", None))
        self.serverStatusLabel.setText(QCoreApplication.translate("MainWindow", u"Server Status:", None))
    # retranslateUi


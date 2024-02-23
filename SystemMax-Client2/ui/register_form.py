# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_form.ui'
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
        self.registerButton = QPushButton(self.centralwidget)
        self.registerButton.setObjectName(u"registerButton")
        self.registerButton.setGeometry(QRect(260, 270, 100, 32))
        self.goToLoginButton = QPushButton(self.centralwidget)
        self.goToLoginButton.setObjectName(u"goToLoginButton")
        self.goToLoginButton.setGeometry(QRect(400, 270, 100, 32))
        self.usernameLineEdit = QLineEdit(self.centralwidget)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")
        self.usernameLineEdit.setGeometry(QRect(250, 120, 261, 21))
        self.nameLineEdit = QLineEdit(self.centralwidget)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QRect(250, 160, 261, 21))
        self.emailLineEdit = QLineEdit(self.centralwidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")
        self.emailLineEdit.setGeometry(QRect(250, 200, 261, 21))
        self.passwordLineEdit = QLineEdit(self.centralwidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setGeometry(QRect(250, 240, 261, 21))
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(280, 80, 261, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(190, 120, 58, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 160, 58, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(190, 200, 58, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(190, 240, 58, 16))
        self.serverStatusLabel = QLabel(self.centralwidget)
        self.serverStatusLabel.setObjectName(u"serverStatusLabel")
        self.serverStatusLabel.setGeometry(QRect(320, 320, 121, 16))
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
        self.registerButton.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.goToLoginButton.setText(QCoreApplication.translate("MainWindow", u"Back to Login", None))
        self.passwordLineEdit.setInputMask("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Please register to SystemMax!", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"username:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"name:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"email:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"password:", None))
        self.serverStatusLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi


from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui.gui import Ui_MainWindow
from components.terminal_widget import TerminalWidget
from enviorment.env import ENV

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.profile_window = None
        self.login_window = None
        self.setupUi(self)
        self.initUI()
        self.initTerminalWidget()

    def initUI(self):
        self.actionLogout.triggered.connect(self.logout)
        self.actionView.triggered.connect(self.viewProfile)

    def initTerminalWidget(self):
        self.terminalWidget = TerminalWidget(self)
        self.terminalLayout.addWidget(self.terminalWidget)

    def viewProfile(self):
        from ProfileWindow import ProfileWindow
        self.profile_window = ProfileWindow()
        self.profile_window.show()

    def logout(self):
        env = ENV()
        env.clear_session()
        QMessageBox.information(self, "Logged Out", "You have been successfully logged out.")
        self.switch_to_login()

    def switch_to_login(self):
        from LoginForm import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

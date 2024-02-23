from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui.gui import Ui_MainWindow
from components.terminal_widget import TerminalWidget
from enviorment.env import ENV

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.initTerminalWidget()

    def initUI(self):
        self.actionLogout.triggered.connect(self.logout)

    def initTerminalWidget(self):
        self.terminalWidget = TerminalWidget(self)
        self.terminalLayout.addWidget(self.terminalWidget)

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

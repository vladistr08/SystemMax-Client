from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.gui import Ui_MainWindow  # Ensure this is the correct import path
from components.terminal_widget import TerminalWidget
from enviorment.env import ENV  # Check this import path too

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup UI from the .ui file
        self.initUI()
        self.initTerminalWidget()

    def initUI(self):
        self.actionLogout.triggered.connect(self.logout)

    def initTerminalWidget(self):
        # Assuming you have a placeholder widget in your UI where the terminal should be
        self.terminalWidget = TerminalWidget(self)
        self.terminalLayout.addWidget(self.terminalWidget)  # Replace 'terminalLayout' with the actual layout name in your UI

    def logout(self):
        env = ENV()
        env.clear_session()
        QMessageBox.information(self, "Logged Out", "You have been successfully logged out.")
        self.switch_to_login()

    def switch_to_login(self):
        from LoginForm import LoginWindow  # Ensure correct import path
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

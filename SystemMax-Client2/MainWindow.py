from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui.gui import Ui_MainWindow
from components.terminal_widget import TerminalWidget
from enviorment.env import ENV
from components.chat_widget import ChatWidget
from api.graphql_client import GraphQLClient

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.chatWidget = None
        self.profile_window = None
        self.login_window = None
        self.graphql_client = GraphQLClient()
        self.setupUi(self)
        self.initUI()
        self.initTerminalWidget()
        self.initChatWidget()

    def initUI(self):
        self.actionLogout.triggered.connect(self.logout)
        self.actionView.triggered.connect(self.viewProfile)

    def initTerminalWidget(self):
        self.terminalWidget = TerminalWidget(self)
        self.terminalLayout.addWidget(self.terminalWidget)

    def initChatWidget(self):
        env = ENV()
        token = env.token
        messages = self.graphql_client.getMessages(chatId="b36052ad-1b47-4786-be05-2faa278ef81d", token=token)
        self.chatWidget = ChatWidget(messages, self)
        self.chatLayout.addWidget(self.chatWidget)

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

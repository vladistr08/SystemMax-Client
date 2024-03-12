from typing import List, Dict

from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from components.chat_search import ChatSearchWidget
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
        self.setupUi(self)  # Assuming this is where you set up the main window layout
        self.initUI()
        self.initTerminalWidget()

        self.stackedWidget = QStackedWidget(self)  # Create a QStackedWidget
        self.initChatSearchWidget()
        self.chatWidget = ChatWidget("", [], self)  # Initially empty

        self.stackedWidget.addWidget(self.chatSearchWidget)
        self.stackedWidget.addWidget(self.chatWidget)  # Add widgets to the stack

        self.chatLayout.addWidget(self.stackedWidget)  # Assuming chatLayout is defined and accessible
        self.chatSearchWidget.chatSelected.connect(self.openChat)
        self.chatSearchWidget.createChat.connect(self.createChat)
        self.chatSearchWidget.chatDeleted.connect(self.deleteChat)

    def updateChats(self, updated_chats: List[Dict[str, str]]):
        self.chats = updated_chats
        self.clearChatCards()
        self.setupUi()

    def clearChatCards(self):
        # Method to remove all chat cards from the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def deleteChat(self, chatId):
        env = ENV()
        token = env.token
        result, errors = self.graphql_client.deleteChat(chatId, token)
        if errors:
            QMessageBox.critical(self, "Error", f"Failed to delete chat: {errors}")
        else:
            QMessageBox.information(self, "Success", f"Chat '{chatId}' deleted successfully.")
            self.refreshChatList()

    def createChat(self, chatName):
        env = ENV()
        token = env.token# Assuming `env` is accessible
        result, errors = self.graphql_client.createChat(chatName, token)
        if errors:
            QMessageBox.critical(self, "Error", f"Failed to create chat: {errors}")
        else:
            QMessageBox.information(self, "Success", f"Chat '{chatName}' created successfully.")
            self.refreshChatList()

    def refreshChatList(self):
        env = ENV()
        self.user_chats = self.graphql_client.getChats(token=env.token)# Fetch the updated list of chats
        self.chatSearchWidget.updateChats(self.user_chats)

    def initChatSearchWidget(self):
        env = ENV()
        self.user_chats = self.graphql_client.getChats(token=env.token)

        self.chatSearchWidget = ChatSearchWidget(self.user_chats, self)
        self.stackedWidget.addWidget(self.chatSearchWidget)  # Add to stacked widget if not already added
        self.chatSearchWidget.chatSelected.connect(self.openChat)

    def initChatWidget(self, chatId, chat):
        messages = self.fetchMessagesForChat(chat["chatId"])
        self.chatWidget = ChatWidget(chatId, messages, self)
        self.stackedWidget.addWidget(self.chatWidget)
        self.chatWidget.backToSearch.connect(self.switchToChatSearch)  # Connect the signal to switch back
        self.stackedWidget.setCurrentWidget(self.chatWidget)

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

    def openChat(self, chatId, chat):
        self.initChatWidget(chatId, chat) # Switch to chat widget

    def fetchMessagesForChat(self, chatId):
        env = ENV()
        token = env.token
        messages = self.graphql_client.getMessages(chatId=chatId, token=token)
        print(chatId)
        print(messages)
        return messages

    def switchToChatSearch(self):
        self.stackedWidget.setCurrentWidget(self.chatSearchWidget)

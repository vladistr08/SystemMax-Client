from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
                               QScrollArea, QLabel, QLineEdit, QMessageBox, QSizePolicy)
from PySide6.QtCore import Slot, Qt, Signal
from enviorment.env import ENV
from api.graphql_client import GraphQLClient
from typing import List, Dict


class ChatWidget(QWidget):
    backToSearch = Signal()  # Signal to notify when to switch back to the chat search widget

    def __init__(self, chatId, messages: List[Dict[str, str]], parent=None):
        super(ChatWidget, self).__init__(parent)
        self.env = ENV()
        self.graphQLClient = GraphQLClient()
        self.setupUi()
        self.chat_history = []
        self.chatId = chatId

        if len(messages) != 0:
            self.messages_sorted = sorted(messages,
                                          key=lambda x: int(x.get('messageIndex', 0)))  # Sort messages by messageIndex
            if self.messages_sorted:
                for message in self.messages_sorted:
                    display = ""
                    if int(message.get("messageIndex", 0)) % 2 == 0:
                        display = self.env.user_data["username"] + ": "
                    else:
                        display = "Assistant: "
                    display += message.get("message", "")
                    self.add_message_to_display(message=display)

    def updateMessages(self, messages: List[Dict[str, str]]):
        # Clear the existing messages from the display
        for i in reversed(range(self.chatDisplayLayout.count())):
            widgetToRemove = self.chatDisplayLayout.itemAt(i).widget()
            if widgetToRemove is not None:
                self.chatDisplayLayout.removeWidget(widgetToRemove)
                widgetToRemove.deleteLater()

        # Assuming messages are sorted or you will sort them as needed
        self.messages_sorted = sorted(messages, key=lambda x: int(x.get('messageIndex', 0)))

        # Repopulate the chat display with the updated list of messages
        for message in self.messages_sorted:
            display = ""
            if int(message.get("messageIndex", 0)) % 2 == 0:
                display = self.env.user_data["username"] + ": "
            else:
                display = "Assistant: "
            display += message.get("message", "")
            self.add_message_to_display(message=display)

        # Scroll to the bottom to ensure the latest message is visible
        self.chatDisplayArea.verticalScrollBar().setValue(self.chatDisplayArea.verticalScrollBar().maximum())

    def setupUi(self):
        # Main layout
        mainLayout = QVBoxLayout(self)

        # Chat display area
        self.chatDisplayArea = QScrollArea()
        self.chatDisplayArea.setWidgetResizable(True)
        self.chatDisplayWidget = QWidget()
        self.chatDisplayLayout = QVBoxLayout(self.chatDisplayWidget)
        self.chatDisplayArea.setWidget(self.chatDisplayWidget)
        mainLayout.addWidget(self.chatDisplayArea)

        # Text input and send button
        self.textInput = QLineEdit(self)
        self.sendButton = QPushButton("Send", self)
        self.sendButton.clicked.connect(self.on_send_clicked)

        # Save and start new chat buttons
        self.saveChatButton = QPushButton("Save Chat", self)
        self.startNewChatButton = QPushButton("Start New Chat", self)
        self.saveChatButton.clicked.connect(self.on_save_chat_clicked)
        self.startNewChatButton.clicked.connect(self.on_start_new_chat_clicked)

        # Layout for input and buttons
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.textInput)
        inputLayout.addWidget(self.sendButton)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.saveChatButton)
        buttonLayout.addWidget(self.startNewChatButton)
        self.backButton = QPushButton("Back", self)
        self.backButton.clicked.connect(self.on_back_clicked)
        mainLayout.addWidget(self.backButton)

        mainLayout.addLayout(inputLayout)
        mainLayout.addLayout(buttonLayout)

    def prepare_context(self):
        return "\n".join(f"{sender}: {message}" for sender, message in self.chat_history)

    @Slot()
    def on_send_clicked(self):
        user_message = self.textInput.text()
        # Display user message
        self.add_message_to_display(self.env.user_data["username"] + ": " + user_message)
        self.textInput.clear()

        context = self.prepare_context()

        chatgpt_response = self.get_chatgpt_response(user_message, context)
        self.add_message_to_display("Assistant: " + chatgpt_response)

    @Slot()
    def on_save_chat_clicked(self):
        # TODO: Implement logic to save the chat to the backend
        pass

    @Slot()
    def on_start_new_chat_clicked(self):
        for i in reversed(range(self.chatDisplayLayout.count())):
            widgetToRemove = self.chatDisplayLayout.itemAt(i).widget()
            self.chatDisplayLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

    def add_message_to_display(self, message):
        label, _, text = message.partition(": ")

        # Determine the message label color based on the sender
        label_html = f"<span style='color: #720455;'>{label}:</span>" if label == "Assistant" else f"<span style='color: green;'>{label}:</span>"

        # Prepare the full message with HTML for styling
        full_message = f"{label_html} {text}"

        # Use QTextEdit for the message to enable text selection and copying
        message_text_edit = QTextEdit()
        message_text_edit.setReadOnly(True)
        message_text_edit.setHtml(
            f"<div style='background-color:#191919; color:#EFECEC; padding:5px;'>{full_message}</div>")
        message_text_edit.setStyleSheet(
            "QTextEdit { background-color: #191919; color: #EFECEC; font-family: 'Fira Code'; border: none; }")
        message_text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_text_edit.setFocusPolicy(Qt.NoFocus)

        # Set the size policy to prevent the QTextEdit from expanding beyond the size of its content
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHeightForWidth(True)
        message_text_edit.setSizePolicy(size_policy)

        # Update the size of the QTextEdit to fit the content
        message_text_edit.document().adjustSize()
        new_height = message_text_edit.document().size().height()
        message_text_edit.setFixedHeight(new_height + 10)  # Add a little extra height for padding

        self.chatDisplayLayout.addWidget(message_text_edit)

        # Scroll to the bottom to show the latest message
        self.chatDisplayArea.verticalScrollBar().setValue(self.chatDisplayArea.verticalScrollBar().maximum())

    def get_chatgpt_response(self, user_message, context) -> str:
        data, errors = self.graphQLClient.getAssistantResponse(user_message, chatId=self.chatId, context=context, token=self.env.token)
        if errors:
            QMessageBox.critical(self, "Error", f"An error occurred: {errors}")
            return f"An error occurred: {errors}"
        else:
            return data['getAssistantResponse']['message']

    @Slot()
    def on_back_clicked(self):
        self.backToSearch.emit()

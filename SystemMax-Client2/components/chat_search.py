from datetime import datetime

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
                               QPushButton, QInputDialog, QSizePolicy, QSpacerItem, QScrollArea, QLineEdit, QMessageBox)
from PySide6.QtCore import Signal, Qt
from typing import List, Dict
from api.graphql_client import GraphQLClient
from enviorment.env import ENV


class ChatSearchWidget(QWidget):
    chatSelected = Signal(str, dict)  # Emitting the whole chat object for flexibility
    chatDeleted = Signal(str)  # Emitting chatId for deletion
    createChat = Signal(str)  # Signal for creating a new chat

    def __init__(self, chats: List[Dict[str, str]], parent=None):
        super(ChatSearchWidget, self).__init__(parent)
        self.graphQLClient = None
        self.chats = chats
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)

        # Create a scroll area for the chat cards
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setStyleSheet("background-color: #222831;border-radius: 10px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scroll

        # This widget will contain the chat cards layout
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Create a layout for the scroll area content
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.scrollAreaLayout)

        # Add chat cards to the scroll area layout
        for chat in self.chats:
            self.addChatCard(chat, self.scrollAreaLayout)

        # Add the scroll area to the main layout
        self.mainLayout.addWidget(self.scrollArea)

        # Create the 'Create Chat' button
        self.createButton = QPushButton("Create Chat")
        self.createButton.setStyleSheet("background-color: #070F2B;border-style: outset;border-width: "
                                        "2px;border-radius: 10px; padding: 6px; font: 300 20pt \"Fira Code\";")
        self.createButton.clicked.connect(self.onCreateButtonClicked)

        # Add the button to the main layout, centered at the bottom
        self.mainLayout.addWidget(self.createButton, 0, Qt.AlignCenter)

    def addChatCard(self, chat, layout):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #333;")
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        frame.setMinimumHeight(60)  # Adjust this value as needed

        # Use QVBoxLayout as the main layout for the frame
        mainFrameLayout = QVBoxLayout(frame)
        #mainFrameLayout.setContentsMargins(5, 5, 5, 5)
        mainFrameLayout.setSpacing(0)

        # Create a QHBoxLayout for the chatNameEdit and deleteButton
        topLayout = QHBoxLayout()
        topLayout.setSpacing(10)  # Adjust spacing as needed

        chatNameEdit = QLineEdit(chat["chatName"])
        chatNameEdit.setStyleSheet("color: white; font-size: 16px; background: #070F2B;  border-style: "
                                   "outset;border-width: 2px;border-radius: 10px; margin: 4px; padding: 5px; width: "
                                   "10em; height: 2em; font: 300 18pt \"Fira Code\";")
        chatNameEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        chatNameEdit.editingFinished.connect(
            lambda: self.onChatNameEditFinished(chat["chatId"], chatNameEdit))

        deleteButton = QPushButton("X")
        deleteButton.setStyleSheet("color: white; background-color: #A0153E;border-style: "
                                   "outset;border-width: 1px;border-radius: 10px; margin: 4px; padding: 5px; "
                                   " height: 1.5em; width: 1.5em; font: 300 12pt \"Fira Code\";")
        deleteButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        deleteButton.setMaximumWidth(70)
        deleteButton.clicked.connect(lambda: self.onDeleteButtonClicked(chat["chatId"]))

        # Add chatNameEdit and deleteButton to the topLayout
        topLayout.addWidget(chatNameEdit)
        topLayout.addStretch()  # This will push the delete button to the right
        topLayout.addWidget(deleteButton)

        # Add the topLayout to the mainFrameLayout
        mainFrameLayout.addLayout(topLayout)

        datetime_obj = datetime.fromisoformat(chat["createdAt"].replace("Z", "+00:00"))
        formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

        timestampLabel = QLabel(formatted_date)
        timestampLabel.setStyleSheet("color: #A0153E; font-size: 14px;font: 300 14pt \"Fira Code\";")
        timestampLabel.setAlignment(Qt.AlignCenter)  # Align the label in the center
        timestampLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add timestampLabel directly below the topLayout in the mainFrameLayout
        mainFrameLayout.addWidget(timestampLabel)

        frame.mousePressEvent = lambda event: self.onChatCardClicked(chatId=chat.get("chatId", ""), chat=chat)

        layout.addWidget(frame)

    def updateChatNameInDb(self, chatId, newChatName):
        self.graphQLClient = GraphQLClient()
        env = ENV()
        token = env.token
        data, errors = self.graphQLClient.updateChat(chatId, chatName=newChatName, token=token)
        if errors:
            QMessageBox.critical(self, "Error", f"Failed to delete chat: {errors}")
        else:
            print("Update succesfully")

    def onChatNameEditFinished(self, chatId, chatNameEdit):
        newChatName = chatNameEdit.text()
        self.updateChatNameInDb(chatId, newChatName)

    def onChatCardClicked(self, chatId, chat):
        self.chatSelected.emit(chatId, chat)

    def onDeleteButtonClicked(self, chatId):
        self.chatDeleted.emit(chatId)

    def onCreateButtonClicked(self):
        chatName, ok = QInputDialog.getText(self, "Create Chat", "Enter chat name:")
        if ok and chatName:
            self.createChat.emit(chatName)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

    def updateChats(self, chats: List[Dict[str, str]]):
        # Clear the layout inside the scroll area
        self.clearLayout(self.scrollAreaLayout)  # Pass the correct layout

        # Update the chat list
        self.chats = chats

        # Rebuild the chat cards
        for chat in self.chats:
            self.addChatCard(chat, self.scrollAreaLayout)

        self.scrollAreaWidgetContents.setLayout(self.scrollAreaLayout)

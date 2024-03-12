from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
                               QPushButton, QInputDialog, QSizePolicy, QSpacerItem, QScrollArea, QLineEdit)
from PySide6.QtCore import Signal, Qt
from typing import List, Dict

from enviorment.env import ENV


class ChatSearchWidget(QWidget):
    chatSelected = Signal(str, dict)  # Emitting the whole chat object for flexibility
    chatDeleted = Signal(str)  # Emitting chatId for deletion
    createChat = Signal(str)  # Signal for creating a new chat

    def __init__(self, chats: List[Dict[str, str]], parent=None):
        super(ChatSearchWidget, self).__init__(parent)
        self.chats = chats
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)

        # Create a scroll area for the chat cards
        self.scrollArea = QScrollArea(self)
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
        self.createButton.clicked.connect(self.onCreateButtonClicked)

        # Add the button to the main layout, centered at the bottom
        self.mainLayout.addWidget(self.createButton, 0, Qt.AlignCenter)

    def addChatCard(self, chat, layout):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: black;")
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        frame.setMinimumHeight(60)  # Adjust this value as needed

        frameLayout = QHBoxLayout(frame)  # Changed to QHBoxLayout
        frameLayout.setContentsMargins(5, 5, 5, 5)
        frameLayout.setSpacing(0)

        self.chatNameEdit = QLineEdit(chat["chatName"])
        self.chatNameEdit.setStyleSheet("color: white; font-size: 16px; background: dark-green; border: none;")
        self.chatNameEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chatNameEdit.editingFinished.connect(
            lambda: self.onChatNameEditFinished(chat["chatId"], self.chatNameEdit))

        timestampLabel = QLabel(chat["createdAt"])
        timestampLabel.setStyleSheet("color: white; font-size: 14px;")  # Increased font size
        timestampLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        deleteButton = QPushButton("Delete")
        deleteButton.setStyleSheet("color: white; background-color: red;")  # Made the button red
        deleteButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        deleteButton.setMaximumWidth(70)  # Set a maximum width for the button
        deleteButton.clicked.connect(lambda: self.onDeleteButtonClicked(chat["chatId"]))

        frameLayout.addWidget(self.chatNameEdit)
        frameLayout.addWidget(timestampLabel)
        frameLayout.addStretch()  # This will push the delete button to the right
        frameLayout.addWidget(deleteButton)

        frame.mousePressEvent = lambda event: self.onChatCardClicked(chatId=chat.get("chatId", ""), chat=chat)

        layout.addWidget(frame)

    def updateChatNameInDb(self, chatId, newChatName):
        print("update chat in db for me!!!!!!!!!!!!!!!!!!!!!")
        pass
        # TODO update db

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

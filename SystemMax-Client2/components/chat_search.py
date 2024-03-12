from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
                               QPushButton, QInputDialog, QSizePolicy)
from PySide6.QtCore import Signal, Qt
from typing import List, Dict

class ChatSearchWidget(QWidget):
    chatSelected = Signal(dict)  # Emitting the whole chat object for flexibility
    chatDeleted = Signal(str)    # Emitting chatId for deletion
    createChat = Signal(str)     # Signal for creating a new chat

    def __init__(self, chats: List[Dict[str, str]], parent=None):
        super(ChatSearchWidget, self).__init__(parent)
        self.chats = chats
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        for chat in self.chats:
            self.addChatCard(chat, layout)

        createButton = QPushButton("Create Chat")
        createButton.clicked.connect(self.onCreateButtonClicked)
        layout.addWidget(createButton)

    def addChatCard(self, chat, layout):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: black;")
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        frame.setMinimumHeight(60)  # Adjust this value as needed

        frameLayout = QHBoxLayout(frame)  # Changed to QHBoxLayout
        frameLayout.setContentsMargins(5, 5, 5, 5)
        frameLayout.setSpacing(0)

        chatNameLabel = QLabel(chat["chatName"])
        chatNameLabel.setStyleSheet("color: white; font-size: 16px;")  # Increased font size
        chatNameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        timestampLabel = QLabel(chat["createdAt"])
        timestampLabel.setStyleSheet("color: white; font-size: 14px;")  # Increased font size
        timestampLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        deleteButton = QPushButton("Delete")
        deleteButton.setStyleSheet("color: white; background-color: red;")  # Made the button red
        deleteButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        deleteButton.setMaximumWidth(70)  # Set a maximum width for the button
        deleteButton.clicked.connect(lambda: self.onDeleteButtonClicked(chat["chatId"]))

        frameLayout.addWidget(chatNameLabel)
        frameLayout.addWidget(timestampLabel)
        frameLayout.addStretch()  # This will push the delete button to the right
        frameLayout.addWidget(deleteButton)

        frame.mousePressEvent = lambda event: self.onChatCardClicked(chat)

        layout.addWidget(frame)

    def onChatCardClicked(self, chat):
        self.chatSelected.emit(chat)

    def onDeleteButtonClicked(self, chatId):
        self.chatDeleted.emit(chatId)

    def onCreateButtonClicked(self):
        chatName, ok = QInputDialog.getText(self, "Create Chat", "Enter chat name:")
        if ok and chatName:
            self.createChat.emit(chatName)

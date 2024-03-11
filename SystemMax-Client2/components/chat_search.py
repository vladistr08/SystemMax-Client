from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Signal
from typing import List, Dict

class ChatSearchWidget(QWidget):
    chatSelected = Signal(dict)  # Emitting the whole chat object for flexibility

    def __init__(self, chats: List[Dict[str, str]], parent=None):
        super(ChatSearchWidget, self).__init__(parent)
        self.chats = chats
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)
        for chat in self.chats:
            self.addChatCard(chat, layout)

    def addChatCard(self, chat, layout):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frameLayout = QVBoxLayout(frame)

        chatNameLabel = QLabel(chat["chatName"])
        timestampLabel = QLabel(chat["timestamp"])
        frameLayout.addWidget(chatNameLabel)
        frameLayout.addWidget(timestampLabel)

        frame.mousePressEvent = lambda event: self.onChatCardClicked(chat)
        layout.addWidget(frame)

    def onChatCardClicked(self, chat):
        self.chatSelected.emit(chat)
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal


class CommandLineEdit(QLineEdit):
    tabPressed = Signal()
    rightArrowPressed = Signal()
    upArrowPressed = Signal()
    downArrowPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.upArrowPressed.emit()
        elif event.key() == Qt.Key_Right:
            self.rightArrowPressed.emit()
        elif event.key() == Qt.Key_Down:
            self.downArrowPressed.emit()
        elif event.key() == Qt.Key_Tab:
            event.accept()
            self.tabPressed.emit()
        else:
            super().keyPressEvent(event)

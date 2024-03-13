from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal


class CommandLineEdit(QLineEdit):
    tabPressed = Signal()
    rightArrowPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            # Emit signal or directly call a method to handle right arrow press
            self.rightArrowPressed.emit()
        elif event.key() == Qt.Key_Tab:
            # Prevent the default focus traversal behavior
            event.accept()
            # Emit a signal or call a method to handle tab completion
            self.tabPressed.emit()
        else:
            super().keyPressEvent(event)

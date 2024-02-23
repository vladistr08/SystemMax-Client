from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal


class CommandLineEdit(QLineEdit):
    tabPressed = Signal()  # Custom signal to indicate a tab was pressed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.tabPressed.emit()  # Emit signal when Tab is pressed
        else:
            super().keyPressEvent(event)  # Handle other key presses normally

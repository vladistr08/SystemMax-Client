import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit

from command_line_edit import CommandLineEdit
from gui import Ui_MainWindow
from terminal_widget import TerminalWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup UI
        self.terminalWidget = TerminalWidget(self)
        self.setCentralWidget(self.terminalWidget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

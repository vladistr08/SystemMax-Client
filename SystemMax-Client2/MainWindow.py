from PySide6.QtWidgets import QApplication, QMainWindow

from ui.gui import Ui_MainWindow
from components.terminal_widget import TerminalWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.terminalWidget = TerminalWidget(self)
        self.setCentralWidget(self.terminalWidget)

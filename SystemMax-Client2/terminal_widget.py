import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextBrowser, QCompleter
from PySide6.QtCore import Slot

from command_line_edit import CommandLineEdit


class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineEdit = None
        self.textBrowser = None
        self.layout = None
        self.initUI()
        self.workingDir = os.getcwd()

    def initUI(self):
        commands = ['cd', 'ls', 'mkdir', 'rm', 'clear', 'touch']

        self.layout = QVBoxLayout(self)
        self.textBrowser = QTextBrowser(self)
        self.lineEdit = CommandLineEdit(self)

        self.layout.addWidget(self.textBrowser)
        self.layout.addWidget(self.lineEdit)

        self.lineEdit.returnPressed.connect(self.onReturnPressed)
        self.lineEdit.tabPressed.connect(self.onTabPressed)

        completer = QCompleter(commands)
        self.lineEdit.setCompleter(completer)
        self.updatePrompt()

    def updatePrompt(self):
        self.textBrowser.append(f"{os.getcwd()} $")

    @Slot()
    def onReturnPressed(self):
        cmd = self.lineEdit.text().strip()
        self.lineEdit.clear()

        if cmd == "clear":
            self.textBrowser.clear()
            self.updatePrompt()
            return

        if cmd.startswith("cd"):
            try:
                os.chdir(cmd.split(maxsplit=1)[1])
                self.workingDir = os.getcwd()
            except Exception as e:
                self.textBrowser.append(str(e))
        else:
            try:
                result = subprocess.check_output(cmd, shell=True, cwd=self.workingDir, text=True,
                                                 stderr=subprocess.STDOUT)
                self.textBrowser.append(result)
            except subprocess.CalledProcessError as e:
                self.textBrowser.append(e.output)
        self.updatePrompt()

    @Slot()
    def onTabPressed(self):
        commands = ['cd', 'ls', 'mkdir', 'rm', 'clear', 'touch']
        currentText = self.lineEdit.text()
        suggestions = [cmd for cmd in commands if cmd.startswith(currentText)]
        if suggestions:
            self.lineEdit.setText(suggestions[0] + ' ')

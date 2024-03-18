import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QCompleter
from PySide6.QtCore import Slot, Qt
from components.command_line_edit import CommandLineEdit
from ansi2html import Ansi2HTMLConverter

class TerminalWidget(QWidget):
    commands = [
        'cd', 'ls', 'mkdir', 'rm', 'clear', 'touch', 'cp', 'mv', 'echo', 'cat',
        'grep', 'find', 'chmod', 'chown', 'export', 'unset', 'env', 'history',
        'kill', 'curl', 'wget', 'tar', 'gzip', 'gunzip', 'zip', 'unzip', 'ssh',
        'scp', 'rsync', 'git', 'npm', 'yarn', 'pip', 'conda', 'awk', 'sed',
        'sort', 'uniq', 'df', 'du', 'free', 'top', 'htop', 'nano', 'vim', 'emacs',
        'tail', 'head', 'less', 'more', 'ping', 'traceroute', 'netstat', 'ifconfig',
        'systemctl', 'journalctl', 'docker', 'kubectl', 'ansible', 'make', 'gcc',
        'g++', 'python', 'python3', 'java', 'javac', 'ruby', 'perl', 'php'
    ]
    def __init__(self, parent=None):
        super().__init__(parent)
        self.converter = Ansi2HTMLConverter(inline=True)  # Create an instance of Ansi2HTMLConverter
        self.lineEdit = None
        self.textBrowser = None
        self.layout = None
        self.initUI()
        self.workingDir = os.getcwd()

    def initUI(self):

        self.layout = QVBoxLayout(self)
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setStyleSheet("background-color: #222831; font: 300 14pt \"Fira Code\";")
        self.lineEdit = CommandLineEdit(self)
        self.lineEdit.setStyleSheet("background-color: #222831;")

        self.layout.addWidget(self.textBrowser)
        self.layout.addWidget(self.lineEdit)

        self.lineEdit.returnPressed.connect(self.onReturnPressed)
        self.lineEdit.tabPressed.connect(self.onTabPressed)
        self.lineEdit.rightArrowPressed.connect(self.onRightArrowPressed)

        completer = QCompleter(self.commands)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.lineEdit.setCompleter(completer)
        self.updatePrompt()

    def updatePrompt(self):
        self.textBrowser.append(f"<p style='color: pink;'>{os.getcwd()}<span style='color: white;'>$</span></p>")

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
                self.textBrowser.append(f"<span style='color: red;'>{str(e)}</span>")
        else:
            try:
                result = subprocess.check_output(cmd, shell=True, cwd=self.workingDir, text=True,
                                                 stderr=subprocess.STDOUT)
                # Convert ANSI to HTML
                html_result = self.converter.convert(result, full=True, ensure_trailing_newline=True)
                self.textBrowser.append(html_result)
            except subprocess.CalledProcessError as e:
                # Convert error output (ANSI to HTML) before appending
                html_error = self.converter.convert(e.output, full=False)
                self.textBrowser.append(f"<p style='color: red;'>{html_error}</p>")
        self.updatePrompt()

    @Slot()
    def onTabPressed(self):
        currentText = self.lineEdit.text().strip()
        parts = currentText.split()

        # Determine if the last word is a path command or part of a path
        path_commands = ['cd', 'ls', 'mkdir', 'rm', 'touch', 'cp', 'mv', 'cat', 'grep', 'find']
        file_commands = []
        if parts and parts[0] in path_commands:
            try:
                dirList = os.listdir(self.workingDir)
                file_commands += dirList  # Append directory contents to the commands list
            except Exception as e:
                print(f"Error accessing directory contents: {e}")

        # Update the completer with the new commands list
        completer = QCompleter(currentText + ' ' + self.commands if len(file_commands) == 0 else file_commands)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)
        self.lineEdit.completer().complete()

    @Slot()
    def onRightArrowPressed(self):
        self.onTabPressed()
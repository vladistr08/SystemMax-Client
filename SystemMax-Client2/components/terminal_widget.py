import os

from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QCompleter
from PySide6.QtCore import Slot, Qt, QThread, Signal
from components.command_line_edit import CommandLineEdit
from ansi2html import Ansi2HTMLConverter

from workers.command_execution import CommandRunner


class TerminalWidget(QWidget):
    actionStop = Signal()

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
        self.converter = Ansi2HTMLConverter(inline=True)
        self.lineEdit = CommandLineEdit(self)
        self.textBrowser = QTextBrowser(self)
        self.layout = QVBoxLayout(self)
        self.workingDir = os.getcwd()
        self.stopShortcut = QShortcut(QKeySequence("Control+C"), self)
        self.stopShortcut.activated.connect(self.terminateCurrentProcess)
        self.initUI()

    def initUI(self):
        self.textBrowser.setStyleSheet("background-color: #222831; font: 300 14pt 'Fira Code';")
        self.lineEdit.setStyleSheet("background-color: #222831;")
        self.layout.addWidget(self.textBrowser)
        self.layout.addWidget(self.lineEdit)
        self.lineEdit.returnPressed.connect(self.onReturnPressed)

        completer = QCompleter(self.commands)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

        self.updatePrompt()

    @Slot()
    def onReturnPressed(self):
        cmd = self.lineEdit.text().strip()
        self.lineEdit.clear()

        if cmd == "clear":
            self.textBrowser.clear()
            self.updatePrompt()
        elif cmd.startswith("cd"):
            try:
                os.chdir(cmd.split(maxsplit=1)[1])
                self.workingDir = os.getcwd()
            except Exception as e:
                self.textBrowser.append(f"<span style='color: red;'>{str(e)}</span>")
        else:
            self.runCommand(cmd)

    def runCommand(self, cmd):
        self.thread = QThread()
        self.commandRunner = CommandRunner(cmd, self.workingDir)
        self.commandRunner.moveToThread(self.thread)

        self.commandRunner.output.connect(self.onCommandOutput, Qt.QueuedConnection)
        self.commandRunner.error.connect(self.onCommandError, Qt.QueuedConnection)
        self.commandRunner.finished.connect(self.onCommandFinished, Qt.QueuedConnection)
        self.commandRunner.finished.connect(self.thread.quit)

        self.thread.started.connect(self.commandRunner.run)
        self.thread.start()

    def onCommandOutput(self, output):
        print(f"Received command output: {output}")
        html_output = self.converter.convert(output, full=True)
        self.textBrowser.append(f"{html_output}")

    def onCommandError(self, error):
        print(f"Received command error: {error}")
        html_error = self.converter.convert(error, full=False)
        self.textBrowser.append(f"<p style='color: red;'>{html_error}</p>")

    def onCommandFinished(self):
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        self.updatePrompt()

    def terminateCurrentProcess(self):
        self.commandRunner.terminate()
        self.textBrowser.append("<p style='color: red;'>Command terminated.</p>")
    def updatePrompt(self):
        self.textBrowser.append(f"<p style='color: pink;'>{os.getcwd()}<span style='color: white;'>$</span></p>")
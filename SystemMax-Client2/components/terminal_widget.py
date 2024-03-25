import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QCompleter, QSizePolicy
from PySide6.QtCore import Qt, QThread, Signal, QObject, QProcess, QTimer
from components.command_line_edit import CommandLineEdit
from ansi2html import Ansi2HTMLConverter

from workers.process_thread import ProcessThread


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
        self.userCommands = ['']
        self.converter = Ansi2HTMLConverter(inline=True)
        self.lineEdit = CommandLineEdit(self)
        self.lineEdit.ctrlCPressed.connect(self.terminateCurrentProcess)
        self.textBrowser = QTextBrowser(self)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(1, 0, 1, 0)
        self.userCommandsIndex = 0

        self.workingDir = os.getcwd()
        self.initUI()
        self.processThread = None
        self.currentThread = None

    def initUI(self):
        self.textBrowser.setStyleSheet("background-color: #222831; font: 300 14pt 'Fira Code'; color: white;")
        self.lineEdit.setStyleSheet("background-color: #333; color: white; margin-top: 0;")

        self.layout.addWidget(self.textBrowser)
        self.layout.addWidget(self.lineEdit)
        self.lineEdit.returnPressed.connect(self.onReturnPressed)
        self.lineEdit.upArrowPressed.connect(self.onUpArrowPressed)
        self.lineEdit.downArrowPressed.connect(self.onDownArrowPressed)

        completer = QCompleter(self.commands, self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)

        self.updatePrompt()

    def onReturnPressed(self):
        cmd = self.lineEdit.text().strip()
        self.lineEdit.clear()

        self.userCommands.append(cmd)

        if cmd == "clear":
            self.textBrowser.clear()
            self.updatePrompt()
        elif cmd.startswith("cd"):
            try:
                os.chdir(cmd.split(maxsplit=1)[1])
                self.workingDir = os.getcwd()
                self.updatePrompt()
            except Exception as e:
                self.textBrowser.append(f"<div style='color: red;'>{e}</div>")
        else:
            if self.currentThread and self.currentThread.isRunning():
                self.processThread.terminate()
                self.currentThread.quit()
                self.currentThread.wait()

            self.processThread = ProcessThread(cmd, self.workingDir)
            self.currentThread = QThread()

            # Move processThread to the currentThread
            self.processThread.moveToThread(self.currentThread)

            # Corrected signal connections
            self.processThread.output.connect(self.onCommandOutput)
            self.processThread.error.connect(self.onCommandError)
            self.processThread.finished.connect(self.onCommandFinished)

            self.currentThread.started.connect(self.processThread.run)
            self.currentThread.start()

    def onUpArrowPressed(self):
        if len(self.userCommands) == 1 or self.userCommandsIndex == len(self.userCommands) - 1:
            return
        self.userCommandsIndex += 1
        self.lineEdit.setText(self.userCommands[-self.userCommandsIndex])

    def onDownArrowPressed(self):
        if len(self.userCommands) == 1 or self.userCommandsIndex == 0:
            return
        self.userCommandsIndex -= 1
        self.lineEdit.setText(self.userCommands[-self.userCommandsIndex])

    def onCommandOutput(self, output):
        html_output = self.converter.convert(output)
        self.textBrowser.append(html_output)

    def onCommandError(self, error):
        html_error = self.converter.convert(error)
        self.textBrowser.append(f"<div style='color: red;'>{html_error}</div>")

    def onCommandFinished(self):
        if self.currentThread:
            self.currentThread.quit()
            self.currentThread.wait()
            self.currentThread = None
        self.updatePrompt()

    def terminateCurrentProcess(self):
        if self.processThread and self.currentThread and self.currentThread.isRunning():
            # Request process termination
            self.processThread.requestTermination.emit()

            # Optionally, implement a delay or a check to confirm termination
            # This part is simplified; actual implementation might require checking process status or capturing termination errors
            QTimer.singleShot(1000, self.checkIfProcessTerminated)  # Check after a delay to give time for termination

        else:
            self.textBrowser.append("<div style='color: red;'>No running process to terminate.</div>")

    def checkIfProcessTerminated(self):
        # This is a placeholder function. You would need to implement actual checks here.
        # For example, check if the port is still in use or if the processThread indicates the process is still running.
        if not self.processThread or self.processThread.runner.process.state() == QProcess.NotRunning:
            self.textBrowser.append("<div style='color: green;'>Process terminated successfully.</div>")

        else:
            self.textBrowser.append(
                "<div style='color: red;'>Process failed to terminate properly. The address might still be in use.</div>")
        self.updatePrompt()

    def updatePrompt(self):
        self.textBrowser.append(f"<div style='color: pink;'>{self.workingDir}$ </div>")
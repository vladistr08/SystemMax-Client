from PySide6.QtCore import QObject, QThread, Signal, QProcess


class CommandRunner(QObject):
    output = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self, command, cwd):
        super().__init__()
        self.command = command
        self.cwd = cwd

    def run(self):
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.setWorkingDirectory(self.cwd)

        # Connect signals for asynchronous I/O
        self.process.readyReadStandardOutput.connect(self.handleStandardOutput)
        self.process.readyReadStandardError.connect(self.handleStandardError)
        self.process.finished.connect(self.handleFinished)

        # Execute the command
        commandParts = self.command.split(" ")
        self.process.start(commandParts[0], commandParts[1:])

    def handleStandardOutput(self):
        if self.process:
            data = self.process.readAllStandardOutput().data().decode()
            self.output.emit(data)

    def handleStandardError(self):
        if self.process:
            data = self.process.readAllStandardError().data().decode()
            if data:
                self.error.emit(data)

    def handleFinished(self, exitCode, exitStatus):
        # Optionally, emit any final messages or perform cleanup
        self.finished.emit()

    def terminate(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.finished.emit()


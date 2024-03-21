from PySide6.QtCore import QProcess, QObject, Signal


class CommandRunner(QObject):
    output = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self, command, cwd):
        super().__init__()
        self.command = command
        self.cwd = cwd
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.setWorkingDirectory(self.cwd)

        self.process.readyReadStandardOutput.connect(self.handleStandardOutput)
        self.process.readyReadStandardError.connect(self.handleStandardError)
        self.process.finished.connect(self.handleFinished)

    def run(self):
        commandParts = self.command.split(" ")
        self.process.start(commandParts[0], commandParts[1:])

    def handleStandardOutput(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.emit(data)

    def handleStandardError(self):
        data = self.process.readAllStandardError().data().decode()
        if data:
            self.error.emit(data)

    def handleFinished(self):
        self.finished.emit()
        self.cleanup()

    def terminate(self):
        if self.process.state() == QProcess.Running:
            self.process.terminate()
            self.cleanup()
            if not self.process.waitForFinished(3000):  # Wait for 3 seconds
                self.process.kill()  # Force kill if not terminated


    def cleanup(self):
        if self.process.state() != QProcess.NotRunning:
            self.process.waitForFinished()

        self.process.close()

from PySide6.QtCore import Signal, QObject, Qt

from workers.command_execution import CommandRunner


class ProcessThread(QObject):
    finished = Signal()
    output = Signal(str)
    error = Signal(str)
    requestTermination = Signal()

    def __init__(self, command, cwd):
        super().__init__()
        self.command = command
        self.requestTermination.connect(self.terminate, Qt.QueuedConnection)
        self.cwd = cwd

    def run(self):
        self.runner = CommandRunner(self.command, self.cwd)
        self.runner.output.connect(self.handleOutput)
        self.runner.error.connect(self.handleError)
        self.runner.error2.connect(self.handleError)
        self.runner.finished.connect(self.cleanup)
        self.runner.run()

    def cleanup(self):
        self.runner.deleteLater()
        self.finished.emit()

    def terminate(self):
        if self.runner:
            self.runner.terminate()

    def handleOutput(self, text):
        self.output.emit(text)

    def handleError(self, text):
        self.error.emit(text)

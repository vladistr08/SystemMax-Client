from PySide6.QtCore import QObject, Signal, QThread

class ChatWorker(QObject):
    finished = Signal(str)  # Signal to emit the response
    error = Signal(str)  # Signal to emit an error

    def __init__(self, user_message, chatId, context, graphQLClient, env):
        super().__init__()
        self.user_message = user_message
        self.chatId = chatId
        self.context = context
        self.graphQLClient = graphQLClient
        self.env = env

    def run(self):
        try:
            data, errors = self.graphQLClient.getAssistantResponse(self.user_message, chatId=self.chatId, context=self.context, token=self.env.token)
            if errors:
                self.error.emit(f"An error occurred: {errors}")
            else:
                self.finished.emit(data['getAssistantResponse']['message'])
        except Exception as e:
            self.error.emit(f"An exception occurred: {str(e)}")
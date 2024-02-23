from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui.login_form import Ui_MainWindow
from api.graphql_client import GraphQLClient
from MainWindow import MainWindow  # Assuming this is the main GUI class
from enviorment.env import ENV


class LoginWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.loginButton.clicked.connect(self.on_login_clicked)
        self.goToRegisterButton.clicked.connect(self.switch_to_register)
        self.graphQLClient = GraphQLClient()
        serverStatusText = "Server Status: online" if self.graphQLClient.verify_connection() else "Server Status: Offline"
        self.serverStatusLabel.setText(serverStatusText)

    def on_login_clicked(self):
        email = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()
        data, errors = self.graphQLClient.loginUser(email, password)

        if errors:
            QMessageBox.critical(self, "Login Failed", str(errors))
        elif data and data.get("loginUser") and data["loginUser"].get("user") and data["loginUser"]["user"].get(
                "user_id"):
            user_data = data["loginUser"]["user"]
            token = data["loginUser"]["token"]

            if not all([user_data.get(key) for key in ["user_id", "username", "email"]]):
                QMessageBox.critical(self, "Login Failed", "Your credentials might not be ok")
                return

            env = ENV()
            env.set_user_data(user_data, token)

            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Unknown error occurred or incomplete response.")

    def switch_to_register(self):
        from RegisterForm import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

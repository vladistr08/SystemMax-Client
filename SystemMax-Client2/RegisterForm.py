from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui.register_form import Ui_MainWindow
from api.graphql_client import GraphQLClient


class RegisterWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(RegisterWindow, self).__init__(parent)
        self.setupUi(self)
        self.registerButton.clicked.connect(self.on_register_clicked)
        self.goToLoginButton.clicked.connect(self.switch_to_login)
        self.graphQLClient = GraphQLClient()
        serverStatusText = "Server Status: online" if self.graphQLClient.verify_connection() else "Server Status: Offline"
        self.serverStatusLabel.setText(serverStatusText)

    def on_register_clicked(self):
            username = self.usernameLineEdit.text()
            email = self.emailLineEdit.text()
            password = self.passwordLineEdit.text()
            name = self.nameLineEdit.text()
            data, errors = self.graphQLClient.createUser(username, email, password, name)

            if errors:
                QMessageBox.critical(self, "Registration Failed", str(errors))
            elif data and data.get("createUser"):
                QMessageBox.information(self, "Registration Successful", "You can now login with your credentials.")
                self.switch_to_login()
            else:
                QMessageBox.warning(self, "Registration Failed", "Unknown error occurred.")

    def switch_to_login(self):
        from LoginForm import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

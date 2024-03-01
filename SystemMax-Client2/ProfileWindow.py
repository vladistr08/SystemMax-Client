from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication
from ui.profile import Ui_MainWindow
from api.graphql_client import GraphQLClient
from enviorment.env import ENV

class ProfileWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ProfileWindow, self).__init__(parent)
        self.setupUi(self)
        self.graphQLClient = GraphQLClient()
        self.env = ENV()
        self.token = self.env.token

        self.initUI()
        self.cancelButton.clicked.connect(self.on_cancel_clicked)
        self.updateButton.clicked.connect(self.update)
        self.actionLogout.triggered.connect(self.logout)

    def initUI(self):
        user, errors = self.graphQLClient.getUser(self.env.user_data['email'])

        if errors:
            QMessageBox.critical(self, "Server Error", "Error retrieving user data:\n" + str(errors))
            return

        if user_data := user.get("getUser", {}).get("user"):
            self.usernameLineEdit.setText(user_data.get("username", ""))
            self.nameLineEdit.setText(user_data.get("name", ""))
            self.emailLineEdit.setText(user_data.get("email", ""))

    def update(self):
        username = self.usernameLineEdit.text()
        name = self.nameLineEdit.text()
        email = self.emailLineEdit.text()

        data, errors = self.graphQLClient.updateUser(self.token, name, username, email)

        if errors:
            QMessageBox.critical(self, "Update Failed", "Failed to update user data:\n" + str(errors))
            return

        if isUpdated := data.get("updateUser", {}).get("isUpdated"):
            QMessageBox.information(self, "Update Successful", "User data updated successfully.")
            user, errors = self.graphQLClient.getUser(email)
            if errors:
                QMessageBox.critical(self, "Error", "Failed to refresh user data:\n" + str(errors))
                return

            if user_data := user.get("getUser", {}).get("user"):
                self.env.clear_session()
                self.env.set_user_data(user_data, self.token)  # Assuming this method exists
                self.env.save_session()
                self.env.load_session()
                self.initUI()
        else:
            QMessageBox.critical(self, "Update Failed", "Cannot update user data.")

    def logout(self):
        self.env.clear_session()
        QMessageBox.information(self, "Logged Out", "You have been successfully logged out.")
        QApplication.instance().closeAllWindows()
        self.switch_to_login()

    def switch_to_login(self):
        from LoginForm import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def on_cancel_clicked(self):
        self.close()

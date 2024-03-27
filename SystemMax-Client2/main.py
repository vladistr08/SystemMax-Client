import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox
from LoginForm import LoginWindow
from MainWindow import MainWindow
from api.graphql_client import GraphQLClient
from enviorment.env import ENV

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("SystemMax")
    app.setWindowIcon(QIcon("/Users/istra/Programare/SystemMax/SystemMax-Client/SystemMax-Client2/res/logo-removebg.png"))

    env = ENV()

    print("Loading session...")
    print(f"Token after loading session: {env.token}")

    graphql_client = GraphQLClient()

    if env.token:
        print("Attempting to refresh token...")
        new_token = graphql_client.refresh_token(env.token)
        print(f"New token: {new_token}")
        if new_token:
            env.set_user_data(env.user_data, new_token)
            print("Showing MainWindow...")
            main_window = MainWindow()
            main_window.show()
        else:
            print("Token refresh failed, showing LoginWindow...")
            login_window = LoginWindow()
            login_window.show()
    else:
        print("No valid session, starting with LoginWindow...")
        login_window = LoginWindow()
        login_window.show()

    sys.exit(app.exec())
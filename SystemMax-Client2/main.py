import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from LoginForm import LoginWindow  # Ensure this import matches the path of your LoginForm module
# from api.graphql_client import GraphQLClient

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # client = GraphQLClient()
    # if not client.verify_connection():
    #     QMessageBox.critical(None, "Server Unavailable", "Unable to connect to the server. Please try again later.")
    #     sys.exit(1)

    loginWindow = LoginWindow()  # Initialize LoginWindow as the starting window
    loginWindow.show()
    sys.exit(app.exec())
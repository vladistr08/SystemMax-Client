from api.graphql_client import GraphQLClient
import json
import os
from datetime import datetime, timedelta
import tempfile

class ENV:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ENV, cls).__new__(cls)
            cls._instance.token = None
            cls._instance.user_data = {}
        return cls._instance
    def __init__(self):
        self.token = None
        self.user_data = {}
        self.graphQLClient = GraphQLClient()
        self.load_session()

    def set_user_data(self, user_data, token):
        self.user_data = user_data
        self.token = token
        self.save_session()

    def save_session(self):
        try:
            session_data = {
                'user_data': self.user_data,
                'token': self.token,
                'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
            }
            temp_file_path = os.path.join(tempfile.gettempdir(), "user_session.json")
            with open(temp_file_path, 'w') as temp_file:
                json.dump(session_data, temp_file)
            print(f"Session saved to {temp_file_path}")
        except Exception as e:
            print(f"Error saving session: {e}")

    def load_session(self):
        try:
            temp_file_path = os.path.join(tempfile.gettempdir(), "user_session.json")
            if os.path.exists(temp_file_path):
                with open(temp_file_path, 'r') as temp_file:
                    session_data = json.load(temp_file)
                    expires_at = datetime.fromisoformat(session_data['expires_at'])
                    if datetime.now() < expires_at - timedelta(minutes=5):  # Check if within 5 minutes of expiring
                        self.user_data = session_data['user_data']
                        self.token = session_data['token']
                        print(f"Session loaded from {temp_file_path}")
                    elif datetime.now() < expires_at:
                        print("Token is close to expiration, attempting to refresh...")
                        graphql_client = GraphQLClient.instance()
                        new_token = graphql_client.refresh_token(self.token)
                        if new_token:
                            self.set_user_data(session_data['user_data'], new_token)
                            print("Token refreshed successfully.")
                        else:
                            print("Token refresh failed, please log in again.")
                            os.remove(temp_file_path)
                    else:
                        print("Session expired, please log in again.")
                        os.remove(temp_file_path)
        except Exception as e:
            print(f"Error loading session: {e}")

    def clear_session(self):
        self.user_data = {}
        self.token = None
        temp_file_path = os.path.join(tempfile.gettempdir(), "user_session.json")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

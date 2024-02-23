import requests
from typing import Tuple

class GraphQLClient:
    def __init__(self, endpoint: str = 'http://localhost:9330/graphql'):
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}

    def execute(self, query: str, variables: dict = None) -> Tuple[dict, dict]:
        try:
            response = requests.post(self.endpoint, json={'query': query, 'variables': variables}, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            data = response_json.get('data', {})
            errors = response_json.get('errors', {})
            return data, errors
        except requests.exceptions.RequestException as e:
            return {}, {"networkError": str(e)}

    def createUser(self, username: str, email: str, password: str, name: str) -> Tuple[dict, dict]:
        query = """
        mutation CreateUser($input: createUserInput!) {
            createUser(input: $input) {
                user {
                    user_id
                    username
                    email
                    name
                }
            }
        }
        """
        variables = {"input": {"username": username, "email": email, "password": password, "name": name}}
        return self.execute(query, variables)

    def loginUser(self, email: str, password: str) -> Tuple[dict, dict]:
        query = """
        query LoginUser($input: loginUserInput!) {
            loginUser(input: $input) {
                user {
                    user_id
                    username
                    email
                }
                token
            }
        }
        """
        variables = {"input": {"email": email, "password": password}}
        return self.execute(query, variables)

    def verify_connection(self) -> bool:
        query = """
        query {
            version
        }
        """
        data, errors = self.execute(query)
        if errors or 'version' not in data:
            return False
        return True

    # Methods for updateUser, logoutUser, getUser, and getAssistantResponse can be similarly defined

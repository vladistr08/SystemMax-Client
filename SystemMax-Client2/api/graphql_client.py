import requests
from typing import Tuple, List, Dict


class GraphQLClient:
    _instance = None

    def __init__(self, endpoint: str = 'http://localhost:9330/graphql'):
        self.endpoint = endpoint

    def __new__(cls, endpoint: str = 'http://localhost:9330/graphql'):
        if cls._instance is None:
            cls._instance = super(GraphQLClient, cls).__new__(cls)
            cls._instance.endpoint = endpoint
        return cls._instance

    def execute(self, query: str, variables: dict = None, token: str = None) -> Tuple[dict, dict]:
        headers = {"Content-Type": "application/json", "authorization": token}
        print({'query': query, 'variables': variables})
        try:
            response = requests.post(self.endpoint, json={'query': query, 'variables': variables}, headers=headers)
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
        return self.execute(query=query, variables=variables)

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
        return self.execute(query=query, variables=variables)

    def verify_connection(self) -> bool:
        query = """
        query {
            version
        }
        """
        data, errors = self.execute(query=query)
        if errors or 'version' not in data:
            return False
        return True

    def refresh_token(self, token: str) -> str:
        query = """
        query refresh {
            refreshToken(input: {token: "%s"}) {
                token
            }
        }
        """ % token

        data, errors = self.execute(query=query)

        if errors:
            print(f"Error refreshing token: {errors}")
            return None

        new_token = None
        if 'refreshToken' in data and 'token' in data['refreshToken']:
            new_token = data['refreshToken']['token']

        return new_token

    def getUser(self, email: str) -> Tuple[dict, dict]:
        query = """
        query GetUser($input: getUserInput!) {
            getUser(input: $input) {
                user {
                    name
                    email
                    user_id
                    username
                    passwordHash
                }
            }
        }
        """
        variables = {"input": {"email": email}}
        return self.execute(query=query, variables=variables)

    def updateUser(self, token: str = None, name: str = None, username: str = None, email: str = None) -> Tuple[dict, dict]:
        assert token is not None
        query = """
        mutation UpdateUser($input: toUpdateUserDataInput!) {
            updateUser(input: $input) {
                isUpdated
            }
        }
        """
        input_vars = {k: v for k, v in
                      [('name', name), ('username', username), ('email', email)] if
                      v is not None}
        variables = {"input": input_vars}
        return self.execute(query, variables, token)

    def getAssistantResponse(self, message: str, context: str, token: str) -> Tuple[dict, dict]:
        query = """
        query GetAssistantResponse($input: getAssistantInput!) {
            getAssistantResponse(input: $input) {
                message
            }
        }
        """
        variables = {
            "input": {
                "message": message + " | This was the user message, please take in considaration this chat history context and dont include in the response anything about this: " + context,
            }
        }
        return self.execute(query=query, variables=variables, token=token)

    def createChat(self, chatName: str, token: str) -> Tuple[dict, dict]:
        print(token)
        mutation = """
        mutation createChat($input: CreateChatInput!) {
            createChat(input: $input) {
                chatId
                isCreated
            }
        }
        """
        variables = {"input": {"chatName": chatName}}
        return self.execute(query=mutation, variables=variables, token=token)

    def deleteChat(self, chatId: str, token: str) -> Tuple[dict, dict]:
        mutation = """
        mutation DeleteChat($input: DeleteChatInput!) {
            removeChat(input: $input) {
                isRemoved
            }
        }
        """
        variables = {"input": {"chatId": chatId}}
        return self.execute(query=mutation, variables=variables, token=token)

    def getChats(self, token: str) -> List[Dict[str, str]]:
        query = """
        query GetChats {
            getUserChatRecords {
                items {
                    chatId
                    chatName
                    createdAt
                }
            }
        }
        """
        data, errors = self.execute(query=query, token=token)
        if errors:
            print(f"Error retrieving chats: {errors}")
            return []

        # Extracting the items array from the response
        items = data.get("getUserChatRecords", {}).get("items", [])

        # Simplify the chat records if needed or directly return items
        chats = []
        for item in items:
            chat_record = {
                "chatId": item.get("chatId", ""),
                "chatName": item.get("chatName", ""),
                "createdAt": item.get("createdAt", "")
            }
            chats.append(chat_record)

        return chats

    def getMessages(self, chatId: str, token: str) -> List[Dict[str, str]]:
        query = """
        query GetMessages($chatId: String!) {
            getUserMessages(input: {chatId: $chatId}) {
                items {
                    message
                    chatId
                    messageIndex
                }
            }
        }
        """
        variables = {"chatId": chatId}
        data, errors = self.execute(query=query, variables=variables, token=token)
        if errors:
            print(f"Error retrieving messages: {errors}")
            return []
        items = data.get("getUserMessages", {}).get("items", [])
        messages = []
        for item in items:
            message_data = {
                "message": item.get("message", ""),
                "chatId": item.get("chatId", ""),
                "messageIndex": item.get("messageIndex", "")
            }
            messages.append(message_data)
        return messages


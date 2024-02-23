class ENV:
    _instance = None

    def __init__(self):
        self.token = None
        self.email = None
        self.username = None
        self.user_id = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ENV, cls).__new__(cls)
            cls.username = None
            cls.user_id = None
            cls.email = None
            cls.token = None
        return cls._instance

    def set_user_data(self, user_data, token):
        self.user_id = user_data.get('user_id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.token = token

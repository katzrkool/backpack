class AuthError(Exception):
    # Incorrect username and password error

    def __init__(self):
        self.message = 'Incorrect username or password!'
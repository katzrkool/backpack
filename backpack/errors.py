class AuthError(Exception):
    # Incorrect username and password error

    def __init__(self):
        self.message = 'Incorrect username or password!'


class MyBackpackBrokeError(Exception):
    # MyBackpack crashed so commonly, we need an error for it

    def __init__(self):
        self.message = 'My Backpack is Broken'
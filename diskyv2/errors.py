class MissingAuth(Exception):
    def __init__(self, message="Token or both Email & Password are required!"):
        self.message = message
        super().__init__(self.message)

class FailedAuth(Exception):
    def __init__(self, message="Login was invalid!"):
        self.message = message
        super().__init__(self.message)
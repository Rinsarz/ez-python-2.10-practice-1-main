class UserNotFoundException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(UserNotFoundException, self).__init__(*args, **kwargs)

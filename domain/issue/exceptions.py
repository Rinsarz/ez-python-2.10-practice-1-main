class IssueNotFoundException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(IssueNotFoundException, self).__init__(*args, **kwargs)

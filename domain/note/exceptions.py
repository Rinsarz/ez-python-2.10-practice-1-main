class NoteNotFoundException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(NoteNotFoundException, self).__init__(*args, **kwargs)

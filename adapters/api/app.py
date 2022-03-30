from domain.user import service as user_service
from domain.issue import service as issue_service
from domain.note import service as note_service
from domain.message import service as message_service
from classic.http_api import App
from adapters.api import controllers

def create_app(
        users: user_service.UserService,
        issues: issue_service.IssueService,
        notes: note_service.NoteService,
        messages: message_service.MessageService,

        ) -> App:
    app = App(prefix='/api')
    user_controller = controllers.UsersResource(users)
    app.register(user_controller)
    app.register(controllers.UserResource(users))
    app.register(controllers.IssueResource(issues))
    app.register(controllers.IssuesResource(issues))
    app.register(controllers.NoteResource(notes))
    app.register(controllers.NotesResource(notes))
    app.register(controllers.MessagesResource(messages))
    app.register(controllers.MessageResource(messages))
    return app
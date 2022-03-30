from wsgiref import simple_server

import falcon
from falcon import App

from adapters.api.controllers import UsersResource, UserResource
from adapters.db.user.storage import UserStorage
from classic.sql_storage import TransactionContext
from domain.user import service as user_service
from domain.issue import service as issue_service
from domain.note import service as note_service
from domain.message import service as message_service
from adapters import api

from sqlalchemy import create_engine
from adapters.db import database


# storage = database.repositories.UserStorage()
# service = UserService(storage=storage)


class Settings:
    db = database.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    users_repo = database.repositories.UsersRepo(context=context)
    issues_repo = database.repositories.IssuesRepo(context=context)
    notes_repo = database.repositories.NotesRepo(context=context)
    messages_repo = database.repositories.MessagesRepo(context=context)


class Application:
    users = user_service.UserService(storage=DB.users_repo)
    issues = issue_service.IssueService(storage=DB.issues_repo)
    notes = note_service.NoteService(storage=DB.notes_repo)
    messages = message_service.MessageService(storage=DB.messages_repo)


class Aspects:
    user_service.join_points.join(DB.context)
    issue_service.join_points.join(DB.context)
    note_service.join_points.join(DB.context)
    api.join_points.join(DB.context)


app = api.create_app(
    users=Application.users,
    issues=Application.issues,
    notes=Application.notes,
    messages=Application.messages
    )

httpd = simple_server.make_server('127.0.0.1', 1234, app)
httpd.serve_forever()
import datetime
import json

import falcon
from falcon import Request

from domain.message.dto import CreateMessageDTO
from .join_points import join_point
from dataclasses import asdict

from adapters.interfaces import UserServiceI, MessageServiceI
from domain.user.dto import UpdateUserDTO, PartiallyUpdateUserDTO, CreateUserDTO
from domain.user.exceptions import UserNotFoundException

from adapters.interfaces import IssueServiceI
from domain.issue.dto import UpdateIssueDTO, PartiallyUpdateIssueDTO, CreateIssueDTO
from domain.issue.exceptions import IssueNotFoundException

from adapters.interfaces import NoteServiceI
from domain.note.dto import CreateNoteDTO, UpdateNoteDTO, PartiallyUpdateNoteDTO
from domain.note.exceptions import NoteNotFoundException


class UserResource:
    def __init__(self, service: UserServiceI):
        self.service = service

    @join_point
    def on_get_user_info(self, req: Request, resp):
        user_id = req.get_param_as_int('user_id')
        try:
            user = self.service.get_user(user_id=user_id)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.body = json.dumps(asdict(user))
        resp.status = falcon.HTTP_200

    @join_point
    def on_post_replace_user(self, req, resp):
        updated_user = req.media
        dto = UpdateUserDTO(**updated_user)
        try:
            self.service.update_user(dto)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    @join_point
    def on_post_change_user(self, req, resp):
        patched_user = req.media
        dto = PartiallyUpdateUserDTO(**patched_user)
        try:
            self.service.partially_update(dto)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    @join_point
    def on_post_delete_user(self, req: Request, resp):
        try:
            self.service.delete_user(**req.media)
        except UserNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class UsersResource:
    def __init__(self, service: UserServiceI):
        self.service = service

    @join_point
    def on_get_show_users(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        order_by = req.get_param('order_by') or None
        users = self.service.get_users(limit=limit, offset=offset, order_by=order_by)
        # или сериализация с помощью pydantic/marshmallow
        # pydantic - быстрее и интерфейс попроще
        res = []
        for u in users:
            res.append(asdict(u))
        resp.body = json.dumps(res)
        resp.status = falcon.HTTP_200

    @join_point
    def on_post_create_user(self, req, resp):
        data = req.get_media()
        new_user = CreateUserDTO(**data)
        user = self.service.create_user(new_user)
        resp.status = falcon.HTTP_201
        resp.location = f'/users/{user.id}'


class IssueResource:
    def __init__(self, service: IssueServiceI):
        self.service = service

    @join_point
    def on_get_show_issue(self, req, resp):
        issue_id = req.get_param_as_int('issue_id')
        try:
            issue = self.service.get_issue(issue_id=issue_id)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)

        issue_dict = asdict(issue)
        for k, v in issue_dict.items():
            if isinstance(v, datetime.datetime):
                issue_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        resp.media = issue_dict
        resp.status = falcon.HTTP_200

    @join_point
    def on_post_replace_issue(self, req, resp):
        updated_issue = req.media
        dto = UpdateIssueDTO(**updated_issue)
        try:
            self.service.update_issue(dto)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    @join_point
    def on_post_change_issue(self, req, resp):
        patched_issue = req.media
        dto = PartiallyUpdateIssueDTO(**patched_issue)
        try:
            self.service.partially_update(dto)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    @join_point
    def on_post_delete_issue(self, req, resp):

        try:
            self.service.delete_issue(**req.media)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class IssuesResource:
    def __init__(self, service: IssueServiceI):
        self.service = service

    @join_point
    def on_get_show_all_issues(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        issues = self.service.get_issues(limit=limit, offset=offset)
        # или сериализация с помощью pydantic/marshmallow
        # pydantic - быстрее и интерфейс попроще
        res = []
        for u in issues:
            issue_dict = asdict(u)
            for k, v in issue_dict.items():
                if isinstance(v, datetime.datetime):
                    issue_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            res.append(issue_dict)
        resp.body = json.dumps(res)
        resp.status = falcon.HTTP_200

    @join_point
    def on_post_create_issue(self, req, resp):
        data = req.get_media()
        # new_issue = CreateIssueDTO(**data)
        issue = self.service.create_issue(**data)
        resp.status = falcon.HTTP_201
        # resp.location = f'/issues/{issue.id}'


class NoteResource:
    def __init__(self, service: NoteServiceI):
        self.service = service

    @join_point
    def on_get_show_note(self, req, resp):
        note_id = req.get_param_as_int('note_id')
        try:
            note = self.service.get_note(note_id)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        note_dict = asdict(note)
        for k, v in note_dict.items():
            if isinstance(v, datetime.datetime):
                note_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        resp.body = json.dumps(note_dict)
        resp.status = falcon.HTTP_200

    @join_point
    def on_post_change_note(self, req, resp):
        updated_note = req.media
        dto = UpdateNoteDTO(**updated_note)
        try:
            self.service.update_note(dto)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    @join_point
    def on_post_update_note(self, req, resp):
        patched_note = req.media
        dto = PartiallyUpdateNoteDTO(**patched_note)
        try:
            self.service.partially_update(dto)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    @join_point
    def on_post_delete_note(self, req, resp):
        try:
            self.service.delete_note(**req.media)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class NotesResource:
    def __init__(self, service: NoteServiceI):
        self.service = service

    @join_point
    def on_get_show_all_notes(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0

        header_filter = req.get_param('header') or None
        tags_filter = req.get_param('tags') or None
        likes_filter = req.get_param('likes') or None
        comments_filter = req.get_param('comments') or None
        filters = {}
        if header_filter is not None:
            filters["header"] = header_filter
        if tags_filter is not None:
            filters["tags"] = tags_filter
        if likes_filter is not None:
            filters["likes"] = likes_filter
        if comments_filter is not None:
            filters["comments"] = comments_filter

        notes = self.service.get_notes(filters=filters, limit=limit, offset=offset)
        # или сериализация с помощью pydantic/marshmallow
        # pydantic - быстрее и интерфейс попроще
        # сделал так чтобы на уроке можно было про это при желании рассказать
        res = []
        for u in notes:
            note_dict = asdict(u)
            for k, v in note_dict.items():
                if isinstance(v, datetime.datetime):
                    note_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            res.append(note_dict)
        resp.body = json.dumps(res)
        resp.status = falcon.HTTP_200

    @join_point
    def on_post_create_note(self, req, resp):
        data = req.get_media()
        new_note = CreateNoteDTO(**data)
        note = self.service.create_note(new_note)
        resp.status = falcon.HTTP_201
        resp.location = f'/notes/{note.id}'


class MessagesResource:
    def __init__(self, service: MessageServiceI):
        self.service = service

    @join_point
    def on_get_show_messages(self, req, resp):
        limit = req.get_param_as_int('limit') or 10
        messages = self.service.get_messages(limit=limit)

        res = []
        for u in messages:
            mesage_dict = asdict(u)
            for k, v in mesage_dict.items():
                if isinstance(v, datetime.datetime):
                    mesage_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            res.append(mesage_dict)
        resp.body = json.dumps(res)
        resp.status = falcon.HTTP_200



    @join_point
    def on_post_create_message(self, req, resp):
        data = req.get_media()
        new_message = CreateMessageDTO(**data)
        message = self.service.create_message(new_message)
        resp.status = falcon.HTTP_201
        resp.location = f'/notes/{message.id}'

class MessageResource:
    def __init__(self, service: MessageServiceI):
        self.service = service

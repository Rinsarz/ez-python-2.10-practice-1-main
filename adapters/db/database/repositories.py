from dataclasses import asdict
from typing import List

from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import select, delete, and_, desc, func

from domain.issue.model import Issue
from domain.message.model import Message
from domain.message.storage import MessageStorageI
from domain.note.model import Note
from domain.user.model import User
from domain.issue import model as issue_models
from domain.user.storage import UserStorageI
from domain.issue.storage import IssueStorageI
from domain.note.storage import NoteStorageI


@component
class NotesRepo(BaseRepository, NoteStorageI):

    def get_one(self, note_id: int):
        return self.session.execute(select(Note).where(Note.id == note_id)).scalars().one_or_none()

    def get_all(self, limit: int, offset: int, filters: dict):
        query = select(Note)
        conditions = []
        text_filters = [tf for tf in ['header', 'text'] if tf in filters]
        number_filters = [nf for nf in ['likes', 'comments'] if nf in filters]
        for tf in text_filters:
            op, val = filters[tf].split(':')
            if op == 'like':
                conditions.append(getattr(Note, tf).like(val))
            elif op == 'eq':
                conditions.append(getattr(Note, tf) == val)
            else:
                raise Exception()

        for nf in number_filters:
            op, val = filters[nf].split(':')
            if op == 'gt':
                conditions.append(getattr(Note, nf) > val)
            elif op == 'lt':
                conditions.append(getattr(Note, nf) < val)
            elif op == 'lte':
                conditions.append(getattr(Note, nf) <= val)
            elif op == 'gte':
                conditions.append(getattr(Note, nf) >= val)
            else:
                raise Exception()
        select_query = query.filter(and_(*conditions))

        notes = self.session.execute(select_query).scalars().all()

        if 'tags' in filters:
            tags = set(filters['tags'].split(','))
            if len(tags) > 0:
                filtered_notes = []
                for note in notes:
                    note_tags = {tag.name for tag in note.tags}
                    if len(tags & note_tags) > 0:
                        filtered_notes.append(note)
                notes = filtered_notes

        return notes[offset: limit + offset]

    def create(self, note: Note):
        self.session.add(note)
        self.session.flush()
        self.session.refresh(note)
        return note

    def update(self, note: Note):
        old_note = self.session.execute(select(Note).where(Note.id == note.id)).scalars().one_or_none()
        old_note.header = note.header
        old_note.text = note.text
        old_note.author_id = note.author_id
        old_note.tags = note.tags
        old_note.likes = note.likes
        old_note.comments = note.comments
        old_note.color = note.color
        old_note.created_date = note.created_date
        old_note.modified_date = note.modified_date
        self.session.flush()

    def delete(self, note_id: int):
        note_old = self.session.query(Note).filter_by(id=note_id).one_or_none()
        self.session.delete(note_old)

    def find_tags(self, tags: List[str]) -> List[issue_models.Tag]:
        tags_query = select(issue_models.Tag). \
            filter(issue_models.Tag.name.in_(tags))
        return self.session.execute(tags_query).scalars().all()


@component
class UsersRepo(BaseRepository, UserStorageI):
    def get_one(self, user_id: int):
        user_query = select(User).where(User.id == user_id)
        return self.session.execute(user_query).scalars().one_or_none()

    def get_all(self, limit: int, offset: int, order_by: str):
        users_query = select(User)
        if order_by is not None:
            if order_by == 'name':
                users_query = users_query.order_by(User.name)
            elif order_by == 'message_time':
                subq = self.session.query(
                    Message.author_id,
                    func.max(Message.created_time).label('last_date')
                    ).group_by(Message.author_id).subquery('t2')
                users_query = select(User).join(subq)\
                    .filter(User.id == subq.c.author_id)\
                    .order_by(desc(subq.c.last_date)) \
                    .distinct(User.id)

        return self.session.execute(users_query).scalars().all()

    def create(self, user: User):
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user

    def update(self, user: User):
        user_old = self.session.query(User).filter_by(id=user.id).one_or_none()
        user_old.name = user.name
        user_old.age = user.age

    def delete(self, user_id: int):
        user_old = self.session.query(User).filter_by(id=user_id).one_or_none()
        self.session.delete(user_old)


@component
class IssuesRepo(BaseRepository, IssueStorageI):
    def get_one(self, issue_id: int):
        issue_query = select(Issue).where(Issue.id == issue_id)
        return self.session.execute(issue_query).scalars().one_or_none()

    def get_all(self, limit: int, offset: int):
        return self.session.execute(select(Issue)).scalars().all()[offset: limit + offset]

    def create(self, issue: Issue):
        self.session.add(issue)
        self.session.flush()
        self.session.refresh(issue)
        return issue

    def update(self, issue: Issue):
        old_issue = self.session.query(Issue).where(Issue.id == issue.id).one_or_none()
        old_issue.tags = issue.tags
        old_issue.status = issue.status
        old_issue.text = issue.text
        old_issue.title = issue.title
        old_issue.assignee_id = issue.assignee_id
        old_issue.author_id = issue.author_id
        old_issue.created_date = issue.created_date
        old_issue.modified_date = issue.modified_date
        self.session.flush()

    def delete(self, issue_id: int):
        issue = self.session.query(Issue).where(Issue.id == issue_id).one_or_none()
        if issue is not None:
            self.session.delete(issue)

    def find_tags(self, tags: List[str]) -> List[issue_models.Tag]:
        tags_query = select(issue_models.Tag). \
            filter(issue_models.Tag.name.in_(tags))
        return self.session.execute(tags_query).scalars().all()


@component
class MessagesRepo(BaseRepository, MessageStorageI):
    def get_one(self, message_id: int):
        message_query = select(Issue).where(Issue.id == message_id)
        return self.session.execute(message_query).scalars().one_or_none()

    def get_all(self, limit: int):
        query = select(Message).order_by(desc(Message.created_time)).limit(limit)
        return self.session.execute(query).scalars().all()

    def create(self, message: Message):
        self.session.add(message)
        self.session.flush()
        self.session.refresh(message)
        return message

    def update(self, message: Message):
        pass

    def delete(self, message_id: int):
        message = self.session.query(Message).where(Message.id == message_id).one_or_none()
        if message is not None:
            self.session.delete(message)
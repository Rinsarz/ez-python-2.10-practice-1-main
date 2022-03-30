from abc import ABC, abstractmethod
from typing import List

from domain.user.dto import *
from domain.user.model import User

from domain.issue.dto import *
from domain.issue.model import Issue

from domain.note.dto import *
from domain.note.model import Note

from domain.message.model import Message
from domain.message.dto import *


class UserServiceI(ABC):
    @abstractmethod
    def get_users(self, limit: int, offset: int, order_by: str) -> List[User]: pass

    @abstractmethod
    def get_user(self, user_id) -> User: pass

    @abstractmethod
    def create_user(self, user: CreateUserDTO) -> User: pass

    @abstractmethod
    def delete_user(self, user_id): pass

    @abstractmethod
    def update_user(self, user: UpdateUserDTO): pass

    @abstractmethod
    def partially_update(self, user: PartiallyUpdateUserDTO): pass


class IssueServiceI(ABC):
    @abstractmethod
    def get_issues(self, limit: int, offset: int) -> List[Issue]: pass

    @abstractmethod
    def get_issue(self, issue_id) -> Issue: pass

    @abstractmethod
    def create_issue(self, issue: CreateIssueDTO) -> Issue: pass

    @abstractmethod
    def delete_issue(self, issue_id): pass

    @abstractmethod
    def update_issue(self, issue: UpdateIssueDTO): pass

    @abstractmethod
    def partially_update(self, issue: PartiallyUpdateIssueDTO): pass


class NoteServiceI(ABC):
    @abstractmethod
    def get_notes(self, filters: dict, limit: int, offset: int) -> List[Note]: pass

    @abstractmethod
    def get_note(self, note_id) -> Note: pass

    @abstractmethod
    def create_note(self, note: CreateNoteDTO) -> Note: pass

    @abstractmethod
    def delete_note(self, note_id): pass

    @abstractmethod
    def update_note(self, note: UpdateNoteDTO): pass

    @abstractmethod
    def partially_update(self, note: PartiallyUpdateNoteDTO): pass


class MessageServiceI(ABC):
    @abstractmethod
    def get_messages(self, limit: int) -> List[Message]: pass

    @abstractmethod
    def get_message(self, note_id) -> Note: pass

    @abstractmethod
    def create_message(self, note: CreateMessageDTO) -> Note: pass

    @abstractmethod
    def delete_message(self, note_id): pass

    @abstractmethod
    def update_message(self, note: UpdateMessageDTO): pass

    @abstractmethod
    def partially_update(self, note: PartiallyUpdateMessageDTO): pass

from abc import ABC, abstractmethod
from typing import List

from domain.issue.model import Tag
from domain.note.model import Note


class NoteStorageI(ABC):

    @abstractmethod
    def get_one(self, note_id: int):
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int, filters:dict):
        pass

    @abstractmethod
    def create(self, note: Note):
        pass

    @abstractmethod
    def update(self, note: Note):
        pass

    @abstractmethod
    def delete(self, note_id: int):
        pass

    @abstractmethod
    def find_tags(self, tags: List[str]) -> List[Tag]:
        pass

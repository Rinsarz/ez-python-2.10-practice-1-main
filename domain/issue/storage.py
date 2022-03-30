from abc import ABC, abstractmethod
from typing import List

from domain.issue.model import Issue
from domain.issue.model import Tag


class IssueStorageI(ABC):

    @abstractmethod
    def get_one(self, issue_id: int):
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int):
        pass

    @abstractmethod
    def create(self, issue: Issue):
        pass

    @abstractmethod
    def update(self, issue: Issue):
        pass

    @abstractmethod
    def delete(self, issue_id: int):
        pass

    @abstractmethod
    def find_tags(self, tags: List[str]) -> List[Tag]:
        pass

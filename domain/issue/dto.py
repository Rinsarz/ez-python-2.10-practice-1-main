import datetime
from dataclasses import dataclass
from typing import List
from classic.app import DTO


class CreateIssueDTO(DTO):
    status: int
    title: str
    text: str
    assignee_id: int
    tags: List[str]
    author_id: int


class UpdateIssueDTO(DTO):
    id: int
    status: int
    title: str
    text: str
    assignee_id: int
    tags: List[str]
    author_id: int
    created_date: str
    modified_date: str


class PartiallyUpdateIssueDTO(DTO):
    id: int
    status: int = None
    title: str = None
    text: str = None
    assignee: str = None
    tags: List[str] = None
    author: str = None

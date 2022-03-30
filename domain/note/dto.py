from dataclasses import dataclass
from typing import List


@dataclass
class CreateNoteDTO:
    header: str
    text: str
    tags: List[str]
    author_id: int
    likes: int
    comments: int
    color: int


@dataclass
class UpdateNoteDTO:
    id: int
    header: str
    text: str
    tags: List[str]
    author_id: int
    likes: int
    comments: int
    created_date: str
    color: int
    modified_date: str


@dataclass
class PartiallyUpdateNoteDTO:
    id: int
    header: str = None
    text: str = None
    tags: List[str] = None
    author_id: int = None
    likes: int = None
    comments: int = None
    color: int = None

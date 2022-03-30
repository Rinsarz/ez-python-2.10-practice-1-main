from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Author:
    id: int
    name: str


@dataclass
class Tag:
    id: int
    name: str


@dataclass
class Assignee:
    id: int
    name: str


@dataclass
class Issue:
    status: int
    title: str
    text: str
    assignee_id: int
    author_id: int
    created_date: datetime
    modified_date: datetime
    tags: List[Tag] = field(default_factory=List)
    id: Optional[int] = None
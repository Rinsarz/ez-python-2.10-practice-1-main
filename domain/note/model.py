import datetime
from dataclasses import dataclass, field
from domain.issue.model import Tag
from typing import List, Optional


@dataclass
class Note:
    header: str
    text: str
    author_id: str
    comments: int
    color: int
    created_date: datetime.datetime
    modified_date: datetime.datetime
    tags: List[Tag] = field(default_factory=List)
    id: Optional[int] = None
    likes: int = 0

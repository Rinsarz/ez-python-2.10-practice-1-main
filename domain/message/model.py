import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Message:
    text: str
    author_id: int
    created_time: datetime.datetime
    id: Optional[int] = None
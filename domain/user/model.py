from dataclasses import dataclass
from typing import Optional

import attr


@dataclass
class User:
    name: str
    age: int
    id: Optional[int] = None

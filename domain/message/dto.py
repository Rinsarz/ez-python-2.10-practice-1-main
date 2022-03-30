import datetime

from classic.app import DTO


class CreateMessageDTO(DTO):
    text: str
    author_id: int


class UpdateMessageDTO(DTO):
    id: int
    text: str
    author_id: int
    created_time: datetime.datetime


class PartiallyUpdateMessageDTO(DTO):
    id: int
    text: str = None
    author: str = None
    created_time: datetime.datetime = None
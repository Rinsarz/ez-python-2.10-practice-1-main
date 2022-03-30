from datetime import datetime
from typing import List

from classic.aspects import PointCut

from adapters.interfaces import MessageServiceI
from domain.message.dto import CreateMessageDTO, UpdateMessageDTO, PartiallyUpdateMessageDTO
from domain.message.model import Message
from domain.note.model import Note
from domain.message.storage import MessageStorageI

join_points = PointCut()
join_point = join_points.join_point


class MessageService(MessageServiceI):
    def __init__(self, storage: MessageStorageI):
        self.storage = storage

    def get_messages(self, limit: int) -> List[Message]:
        messages = self.storage.get_all(limit=limit)
        return messages

    def get_message(self, message_id) -> Note:
        pass

    def create_message(self, message: CreateMessageDTO) -> Message:
        message = Message(
            **message.__dict__,
            created_time=datetime.utcnow()
            )
        return self.storage.create(message=message)

    def delete_message(self, message_id):
        pass

    def update_message(self, message: UpdateMessageDTO):
        pass

    def partially_update(self, message: PartiallyUpdateMessageDTO):
        pass
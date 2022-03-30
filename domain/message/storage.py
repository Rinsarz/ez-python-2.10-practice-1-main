from abc import ABC, abstractmethod
from domain.message.model import Message


class MessageStorageI(ABC):

    @abstractmethod
    def get_one(self, message_id: int):
        pass

    @abstractmethod
    def get_all(self, limit: int):
        pass

    @abstractmethod
    def create(self, message: Message):
        pass

    @abstractmethod
    def update(self, message: Message):
        pass

    @abstractmethod
    def delete(self, message_id: int):
        pass
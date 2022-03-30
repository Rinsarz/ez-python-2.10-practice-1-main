from abc import ABC, abstractmethod

from domain.user.model import User


class UserStorageI(ABC):

    @abstractmethod
    def get_one(self, user_id: int):
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int, order_by: str):
        pass

    @abstractmethod
    def create(self, user: User):
        pass

    @abstractmethod
    def update(self, user: User):
        pass

    @abstractmethod
    def delete(self, user_id: int):
        pass

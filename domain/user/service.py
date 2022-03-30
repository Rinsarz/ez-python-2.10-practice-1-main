from datetime import datetime
from typing import List

from classic.aspects import PointCut

from adapters import interfaces
from domain.user.dto import CreateUserDTO, UpdateUserDTO, PartiallyUpdateUserDTO
from domain.user.exceptions import UserNotFoundException
from domain.user.model import User
from domain.user.storage import UserStorageI

join_points = PointCut()
join_point = join_points.join_point


class UserService(interfaces.UserServiceI):
    def __init__(self, storage: UserStorageI):
        self.storage = storage

    @join_point
    def get_users(self, limit: int, offset: int, order_by: str) -> List[User]:
        # in real life any filters or something else
        users = self.storage.get_all(limit, offset, order_by=order_by)
        return users

    @join_point
    def get_user(self, user_id) -> User:
        user = self.storage.get_one(user_id=user_id)
        if user is None:
            raise UserNotFoundException('user not found')
        return user

    @join_point
    def create_user(self, user: CreateUserDTO) -> User:
        user = User(name=user.name, age=user.age)
        return self.storage.create(user=user)

    @join_point
    def delete_user(self, user_id: str) -> None:
        self.storage.delete(user_id=int(user_id))

    @join_point
    def update_user(self, user: UpdateUserDTO):
        user = User(id=user.id, name=user.name, age=user.age)
        self.storage.update(user=user)

    @join_point
    def partially_update(self, user: PartiallyUpdateUserDTO):
        old_user = self.get_user(user.id)
        if user.name is not None:
            old_user.name = user.name
        if user.age is not None:
            old_user.age = user.age

        self.storage.update(user=old_user)



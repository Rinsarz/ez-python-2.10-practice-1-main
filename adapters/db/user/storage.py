from domain.user.exceptions import UserNotFoundException
from domain.user.model import User
from domain.user.storage import UserStorageI

users_data = {
    '1': User(id=1,name="Jonh Doe",age=30),
    '2': User(id=2,name="Diana Doe",age=28),
    '3': User(id=3,name="Ivanov Ivan",age=22),
    '4': User(id=4,name="Lion Litvions",age=29),
    '5': User(id=5,name="Oleg Ivanov",age=32)
}


class UserStorage(UserStorageI):

    def create(self, user: User):
        new_user_id = len(users_data.keys())+1
        users_data[str(new_user_id)] = user
        user.id = new_user_id
        return user

    def update(self, user: User):
        if str(user.id) not in users_data.keys():
            raise UserNotFoundException(message="user not found")
        users_data.update({str(user.id): user})
        return user

    def delete(self, user_id: int):
        try:
            users_data.pop(str(user_id))
        except KeyError as e:
            raise UserNotFoundException(message="user not found")

    def get_one(self, user_id: str):
        try:
            return users_data[str(user_id)]
        except KeyError as e:
            raise UserNotFoundException(message="user not found")

    def get_all(self, limit: int, offset: int):
        users = list(users_data.values())[offset:limit + offset]
        return users


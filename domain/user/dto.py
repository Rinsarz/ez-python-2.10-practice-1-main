from dataclasses import dataclass


@dataclass
class CreateUserDTO:
    name: str
    age: int


@dataclass
class UpdateUserDTO:
    id: int
    name: str
    age: int


@dataclass
class PartiallyUpdateUserDTO:
    id: int
    name: str = None
    age: int = None

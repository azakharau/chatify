import dataclasses
from typing import Optional


@dataclasses.dataclass()
class User:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[int] = None


class Message:
    ...


class Chat:
    ...


class ChatList:
    ...

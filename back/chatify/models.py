import dataclasses
from typing import Optional

from ..mixins import DataMixin

@dataclasses.dataclass()
class User(DataMixin):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[int] = None


class Message(DataMixin):
    ...


class Chat(DataMixin):
    ...


class ChatList(DataMixin):
    ...

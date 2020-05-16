import typing
from dataclasses import dataclass

from utils.mixins import DataMixin


@dataclass(frozen=False)
class Chat(DataMixin):
    id: typing.Optional[int] = None
    username: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None


@dataclass(frozen=False)
class Message(DataMixin):
    """This object represents a Telegram message."""
    message_id: typing.Optional[int] = None
    from_user: typing.Optional[User] = None
    chat: typing.Optional[Chat] = None
    date: typing.Optional[int] = None
    text: typing.Optional[str] = None

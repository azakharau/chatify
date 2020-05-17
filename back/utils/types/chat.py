import typing
from dataclasses import dataclass

from utils.mixins import DataMixin


@dataclass()
class Chat(DataMixin):
    id: typing.Optional[int] = None
    username: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None

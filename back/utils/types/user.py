import typing
from dataclasses import dataclass

from utils.mixins import DataMixin


@dataclass()
class User(DataMixin):
    id: typing.Optional[int] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    username: typing.Optional[str] = None

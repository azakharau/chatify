from dataclasses import dataclass
from typing import Optional

from utils.mixins import DataMixin


@dataclass()
class Profile(DataMixin):
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    def check_password(self, password: str):
        return self.password == password

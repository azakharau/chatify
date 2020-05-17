from dataclasses import dataclass
from typing import Optional, List, Union

from motor.motor_asyncio import AsyncIOMotorClient

from utils import clean_data
from utils.mixins import DataMixin


@dataclass()
class Profile(DataMixin):
    """Container for user data"""
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    contacts: Optional[Union[List[dict], List[str]]] = None
    chat_id: Optional[str] = None

    def check_password(self, password: str) -> bool:
        return self.password == password

    async def is_user_exist(self,
                            db: AsyncIOMotorClient,
                            request_data: dict) -> bool:
        """
        Check is user document exist in db.
        Args:
            db: db client instance.
            request_data: dict with user data

        Returns:

        """
        email = await db.users.find_one(
            {"email": request_data['email']})

        username = await db.users.find_one(
            {"username": request_data['username']})

        return email or username

    async def fetch_contacts(self,
                             db: AsyncIOMotorClient) -> None:
        """
        Iterate by contacts array, find specific user in db by user_id
        and replace user_id in array by user document from db
        Args:
            db: db client instance.

        """
        for idx, contact in enumerate(self.contacts):
            _contact = await db.users.find_one(
                {"user_id": contact}
            )
            del _contact['contacts']
            del _contact['chat_id']
            self.contacts[idx] = clean_data(_contact)

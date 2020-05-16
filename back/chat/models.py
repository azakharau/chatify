from dataclasses import dataclass
from typing import Optional, List, Union

from profile.models import Profile
from utils import clean_data
from utils.mixins import DataMixin


@dataclass(frozen=False)
class Chat(DataMixin):
    """This object represents a chat object."""
    chat_id: Optional[int] = None
    users: Optional[List[int]] = None
    type: Optional[str] = None
    messages: Optional[Union[List[dict], List[str]]] = None

    async def fetch_messages(self,
                             db):
        for idx, message in enumerate(self.messages):
            _message = await db.messages.find_one(
                {"message_id": message}
            )

            self.messages[idx] = clean_data(_message)


@dataclass(frozen=False)
class ChatList(DataMixin):
    chats: Optional[List[Chat]] = None


@dataclass(frozen=False)
class Message(DataMixin):
    """This object represents a message."""
    message_id: Optional[int] = None
    from_user: Optional[Profile] = None
    date: Optional[int] = None
    text: Optional[str] = None

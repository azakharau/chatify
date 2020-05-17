from datetime import datetime
from typing import Union, Optional

from aiohttp import web

from chat.models import Chat, Message
from profile.models import Profile
from utils import clean_data, get_next_sequence_value


class LoginView(web.View):
    """View class for login form

    Endpoint: /login

    """

    async def post(self) -> Union[web.json_response, web.HTTPException]:
        """
        Take user credentials and check if user exist.
        If exist - return his profile in JSON. Else -> HTTPException
        Returns: User profile or Exception

        """
        request_data = await self.request.json()

        result = await self.find_user(request_data)

        if not result:
            raise web.HTTPNotFound(text="User not found")

        profile = Profile(**clean_data(result))

        if profile.check_password(request_data['password']):
            await profile.fetch_contacts(self.request.app['db'])

            return web.json_response(profile.to_dict(), status=200)

        raise web.HTTPNotAcceptable(text="Wrong password")

    async def find_user(self, request_data: dict) -> Optional[dict]:
        """
        Find user by email or username. If none of this are specified,
        return None.
        Args:
            request_data: dict with login data from request object.

        Returns: User document in db or None

        """
        user = None
        if "username" in request_data:
            user = await self.request.app['db'].users.find_one(
                {'username': request_data["username"]})
        elif "email" in request_data:
            user = await self.request.app['db'].users.find_one(
                {'email': request_data["email"]})
        return user


class RegisterView(web.View):
    """View class for login form

    Endpoint: /register

    """

    async def post(self) -> Union[web.json_response, web.HTTPException]:

        request_data = await self.request.json()

        if await self.is_user_exist(request_data):
            raise web.HTTPConflict(text="User already exist")

        data = await self.prepare_db_request(request_data)

        result = await self.request.app['db'].users.insert_one(data)

        if result:
            return web.Response(text="User create successfully",
                                status=200)
        raise web.HTTPError(text="Unexpected error")

    async def prepare_db_request(self, data: dict) -> dict:
        """
        Prepare request to db. Replace Profile.user_id to int32 value from db.
        Args:
            data: dict with user data for Profile object.

        Returns:  dict with user profile.

        """
        profile = Profile(**data)
        profile.user_id = await get_next_sequence_value(self.request.app['db'],
                                                        "user_id")
        return profile.to_dict()

    async def is_user_exist(self, request_data):
        email = await self.request.app['db'].users.find_one(
            {"email": request_data['email']})

        username = await self.request.app['db'].users.find_one(
            {"username": request_data['username']})

        return email or username


class WebsocketChat(web.View):
    """View class for login form

    Endpoint: /chat/{chat_id}

    """
    async def get(self):
        """
        Initialize websocket connection and handle all received messages.

        """
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        chat_id = int(self.request.match_info.get('chat_id'))
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    message = Message(message_id=await get_next_sequence_value(
                        self.request.app['db'],
                        "message_id"),
                                      chat_id=chat_id,
                                      from_user=1,
                                      to_user=2,
                                      date=datetime.now().strftime(
                                          "%Y.%m.%d - %H:%M:%S"),
                                      text=msg.data)
                    await self.request.app[
                        'db'].messages.insert_one(
                        message.to_dict())
                    await self.request.app['db'].chats.update_one(
                        {'chat_id': message.chat_id},
                        {'$push': {'messages': message.message_id}})
                    await ws.send_json(message.to_dict())

    async def post(self) -> Union[web.json_response, web.HTTPException]:
        """
        Find all messages by chat_id and move it into Chat container object.
        Returns: JSON compiled from Chat object or HTTPException.

        """
        chat_id = int(self.request.match_info.get('chat_id'))

        chat = await self.request.app['db'].chats.find_one(
            {"chat_id": chat_id}
        )
        if not chat:
            raise web.HTTPNotFound(text="Empty chat")
        chat = Chat(**clean_data(chat))
        await chat.fetch_messages(self.request.app['db'])
        return web.json_response(chat.to_dict(), status=200)

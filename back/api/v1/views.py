import json

from aiohttp import web

from profile.models import Profile
from utils import clean_data, get_next_sequence_value


class LoginView(web.View):
    async def get(self):
        return web.json_response({}, status=200)

    async def post(self):
        request_data = await self.request.json()

        result = await self.request.app['db'].users.find_one(
            {'username': request_data["username"]})

        if not result:
            raise web.HTTPNotFound(text="User not found")

        profile = Profile(**clean_data(result))

        if profile.check_password(request_data['password']):
            await profile.fetch_contacts(self.request.app['db'])

            raise web.HTTPFound(f'/dashboard/{profile.user_id}',
                                content_type="application/json",
                                body=json.dumps(profile.to_dict()))

        raise web.HTTPNotAcceptable(text="Wrong password")


class RegisterView(web.View):
    async def get(self):
        return web.json_response({}, status=200)

    async def post(self):

        request_data = await self.request.json()

        if await self.is_user_exist(request_data):
            raise web.HTTPConflict(text="User already exist")

        data = await self.prepare_db_request(request_data)

        result = await self.request.app['db'].users.insert_one(data)

        if result:
            return web.Response(text="User create successfully",
                                status=200)
        raise web.HTTPError(text="Unexpected error")

    async def prepare_db_request(self, data):
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


class DashboardView(web.View):
    async def get(self):
        user_id = self.request.match_info.get('user_id')


class WebsocketChat(web.View):
    async def get(self):
        chat_id = self.request.match_info.get('chat_id')

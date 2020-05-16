from aiohttp import web

from profile.models import Profile
from utils import clean_data


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
            return web.json_response(profile.to_dict(), status=200)
        raise web.HTTPNotAcceptable(text="Wrong password")

    def check_password(self,
                       profile: Profile,
                       password: str):
        return profile.password == password


class RegisterView(web.View):
    async def get(self):
        return web.json_response({}, status=200)

    async def post(self):

        request_data = await self.request.json()

        if await self.is_user_exist(request_data):
            raise web.HTTPConflict(text="User already exist")

        result = await self.request.app['db'].users.insert_one(
            await self.prepare_db_request(request_data))

        if result:
            return web.json_response(text="User create successfully",
                                     status=200)
        raise web.HTTPError(text="Unexpected error")

    async def get_next_sequence_value(self):
        sequence = await self.request.app['db'].counters.find_one_and_update(
            {"_id": "user_id"},
            {"$inc": {"sequence_value": 1}}, new=True)
        return sequence['sequence_value']

    async def prepare_db_request(self, data):
        profile = Profile(**data)
        profile.user_id = await self.get_next_sequence_value()
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

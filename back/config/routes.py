from aiohttp import web


def setup_routes(app: web.Application):
    app.router.add_view('/login', app["handlers"]['login'])
    app.router.add_view('/register', app['handlers']['register'])
    app.router.add_view('/dashboard/{user_id}', app["handlers"]['dashboard'])
    app.router.add_view('/chat/{chat_id}', app["handlers"]['chat'])

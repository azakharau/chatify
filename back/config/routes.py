from aiohttp import web


def setup_routes(app: web.Application):
    app.router.add_view('/login',
                        app["handlers"]['login'],
                        name='login')
    app.router.add_view('/register',
                        app['handlers']['register'],
                        name='register')
    app.router.add_view('/chat/{chat_id}',
                        app["handlers"]['chat'],
                        name='chat')

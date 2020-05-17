from api.v1.views import (LoginView,
                          WebsocketChat,
                          RegisterView)


def setup_handlers(app):
    app['handlers'] = {
        'login': LoginView,
        'register': RegisterView,
        'chat': WebsocketChat
    }



from api.v1.views import (LoginView,
                          DashboardView,
                          WebsocketChat,
                          RegisterView)


def setup_handlers(app):
    app['handlers'] = {
        'login': LoginView,
        'register': RegisterView,
        'dashboard': DashboardView,
        'chat': WebsocketChat
    }



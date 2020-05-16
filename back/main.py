import weakref

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from config import setup_routes, config
from utils.setup_handlers import setup_handlers


async def init_db(app):
    db_client = AsyncIOMotorClient(config.DB_URL)
    app['db'] = db_client[config.DB_NAME]


app = web.Application()
app['websockets'] = weakref.WeakSet()
app.on_startup.append(init_db)

setup_handlers(app)
setup_routes(app=app)

if __name__ == '__main__':
    web.run_app(app, port=8000)

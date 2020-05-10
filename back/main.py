if __name__ == '__main__':
    from aiohttp import web

    app = web.Application()

    web.run_app(app, port=8000)
from aiohttp import web

from boggle import routes


def create_app() -> web.Application:
    application = web.Application()
    routes.init(application)
    return application

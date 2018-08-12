from aiohttp import web

from boggle import database, routes


def create_application() -> web.Application:
    application = web.Application(
        middlewares=[database.session_middleware],
    )
    routes.init(application)
    return application

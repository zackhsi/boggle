import logging

from aiohttp import web

logger = logging.getLogger(__name__)


async def echo(req: web.Request) -> web.Response:
    payload = await req.json()
    return web.json_response(payload)


def init(app: web.Application) -> None:
    logger.info('Initializing routes...')
    app.router.add_post('/echo', echo)

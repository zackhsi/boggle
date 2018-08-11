import logging

from aiohttp import web
from sqlalchemy.orm.session import Session

from boggle.models.game import Game

logger = logging.getLogger(__name__)


async def get(request: web.Request, session: Session) -> web.Response:
    logger.info('GET /games')
    games = session.query(Game).all()
    return web.json_response([str(game.id) for game in games])


async def post(request: web.Request, session: Session) -> web.Response:
    logger.info('POST /games')
    game = Game()
    session.add(game)
    logger.info(f'Created game {game}')
    return web.json_response({})

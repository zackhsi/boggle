import logging

from aiohttp import web
from sqlalchemy.orm.session import Session

from boggle.models.game import Game

logger = logging.getLogger(__name__)


async def get(request: web.Request) -> web.Response:
    session: Session = request.session
    games = session.query(Game).filter_by(**request.query).all()
    return web.json_response([str(game.id) for game in games])


async def post(request: web.Request) -> web.Response:
    session: Session = request.session
    game = Game()
    session.add(game)
    session.flush()
    logger.info(f'Created game {game.id}')
    return web.json_response({'id': str(game.id)})

import logging

from aiohttp import web
from sqlalchemy.orm.session import Session

from boggle.models.game import Game
from boggle.schemas.game import game_schema

logger = logging.getLogger(__name__)


async def get(request: web.Request) -> web.Response:
    session: Session = request.session
    games = session.query(Game).filter_by(**request.query).all()
    return web.json_response({
        'games': [
            game_schema.dump(game).data
            for game in games
        ]
    })


async def post(request: web.Request) -> web.Response:
    session: Session = request.session
    game = Game()
    session.add(game)
    session.flush()
    logger.info(f'Created game {game.id}')
    return web.json_response(game_schema.dump(game).data)


async def put(request: web.Request) -> web.Response:
    session: Session = request.session
    game_id = request.match_info['game_id']
    game = session.query(Game).filter_by(id=game_id).first()
    data = await request.json()
    for key, value in data.items():
        logger.info(
            f'Updating game {game.id} "{key}" from {getattr(game, key)} to '
            f'{value}'
        )
        setattr(game, key, value)
    return web.json_response(game_schema.dump(game).data)

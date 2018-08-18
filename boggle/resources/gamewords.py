import logging

from aiohttp.web import Request, Response
from sqlalchemy.orm.session import Session

from boggle.models.game import Game
from boggle.settings import BOARD_SIZE

logger = logging.getLogger(__name__)


async def post(request: Request) -> Response:
    session: Session = request.session
    game_id = request.match_info['game_id']
    game = session.query(Game).filter_by(id=game_id).first()
    board = game.board
    data = await request.json()
    word = data.get('word')
    if not word or len(word) > BOARD_SIZE:
        return Response(status=400)
    if word in board:
        return Response(status=204)
    else:
        return Response(status=404)

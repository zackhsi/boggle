import logging

from aiohttp.web import Request, Response, json_response
from sqlalchemy.orm.session import Session

from boggle import dictionary
from boggle.models.game import Game
from boggle.settings import (
    BOARD_SIZE,
    REASON_NOT_IN_BOARD_FMT,
    REASON_NOT_IN_DICTIONARY_FMT,
)

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

    # Check dictionary before board so we have saner error messages.
    if not dictionary.lookup(word):
        return json_response(
            {
                'reason': REASON_NOT_IN_DICTIONARY_FMT.format(word=word),
            },
            status=404,
        )
    if word not in board:
        return json_response(
            {
                'reason': REASON_NOT_IN_BOARD_FMT.format(word=word),
            },
            status=404,
        )
    return Response(status=204)

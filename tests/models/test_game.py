from datetime import datetime, timedelta

from freezegun import freeze_time

from boggle import settings
from boggle.models.game import COMPLETED, CREATED, IN_PROGRESS, Game


def test_game_status():
    initial_datetime = datetime(
        year=1991, month=10, day=17, hour=3,
        minute=0, second=0,
    )
    with freeze_time(initial_datetime) as frozen_datetime:
        game = Game()
        assert game.status == CREATED
        game.start()
        assert game.status == IN_PROGRESS
        frozen_datetime.tick(delta=timedelta(
            milliseconds=settings.DEFAULT_GAME_DURATION_MS - 1)
        )
        assert game.status == IN_PROGRESS
        frozen_datetime.tick(delta=timedelta(milliseconds=1))
        assert game.status == COMPLETED

from datetime import datetime, timedelta

from boggle import settings

CREATED = 'created'
IN_PROGRESS = 'in_progress'
COMPLETED = 'completed'


class Game:
    def __init__(self):
        self.started_at = None

    def start(self) -> None:
        self.started_at = datetime.utcnow()

    @property
    def status(self) -> str:
        if not self.started_at:
            return CREATED
        end_time = self.started_at + timedelta(
            milliseconds=settings.DEFAULT_GAME_DURATION_MS,
        )
        if datetime.utcnow() < end_time:
            return IN_PROGRESS
        return COMPLETED

import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, Date
from sqlalchemy.dialects.postgresql import UUID

from boggle import settings
from boggle.database import Base

CREATED = 'created'
IN_PROGRESS = 'in_progress'
COMPLETED = 'completed'


class Game(Base):
    __tablename__ = 'games'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    started_at = Column(Date)

    def __init__(self) -> None:
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

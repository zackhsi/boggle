import logging
import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from boggle import settings
from boggle.database import Base
from boggle.models.board import Board

logger = logging.getLogger(__name__)

CREATED = 'created'
IN_PROGRESS = 'in_progress'
COMPLETED = 'completed'


class Game(Base):
    __tablename__ = 'games'

    id = Column(
        UUID(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    board = relationship(Board, uselist=False)
    created_at = Column(Date)
    started_at = Column(Date)

    def __init__(self) -> None:
        self.created_at = datetime.utcnow()

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

    @property
    def started(self) -> bool:
        return bool(self.started_at)

    @started.setter
    def started(self, new_started: bool) -> None:
        if new_started and not self.started_at:
            self.board = Board()
            self.started_at = datetime.utcnow()
            logger.info(f'Started game {self}')

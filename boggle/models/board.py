import random
import uuid
from typing import Optional

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from boggle.database import Base

# Original UK version (c1976, yellow box)!
# https://gist.github.com/samdobson/6b9a71b39637538338c7e88ced6eb056
DICE = [
    'AACIOT', 'ABILTY', 'ABJMOQ', 'ACDEMP', 'ACELRS', 'ADENVZ', 'AHMORS',
    'BIFORX', 'DENOSW', 'DKNOTU', 'EEFHIY', 'EGKLUY', 'EGINTV', 'EHINPS',
    'ELPSTU', 'GILRUW',
]


class Board(Base):
    __tablename__ = 'boards'

    id = Column(
        UUID(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    game_id = Column(UUID(), ForeignKey('games.id'))
    letters = Column(String)

    def __init__(self, board_string: Optional[str] = None) -> None:
        if board_string:
            letters = board_string.split(', ')
            if len(letters) != 16:
                raise ValueError('Board requires 16 letters')
        else:
            letters = [random.choice(die) for die in DICE]
        self.letters = ''.join(letters)

    def __str__(self) -> str:
        return (
            f'self.letters[0:4]\n'
            f'self.letters[4:8]\n'
            f'self.letters[8:12]\n'
            f'self.letters[12:16]\n'
        )

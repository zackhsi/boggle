import random
import uuid
from typing import Dict, List, Optional, Set

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from boggle.database import Base
from boggle.settings import WILDCARD

# Original UK version (c1976, yellow box)!
# https://gist.github.com/samdobson/6b9a71b39637538338c7e88ced6eb056
DICE = [
    'AACIOT', 'ABILTY', 'ABJMOQ', 'ACDEMP', 'ACELRS', 'ADENVZ', 'AHMORS',
    'BIFORX', 'DENOSW', 'DKNOTU', 'EEFHIY', 'EGKLUY', 'EGINTV', 'EHINPS',
    'ELPSTU', 'GILRUW',
]

#   x
# y 0  1  2  3
#   4  5  6  7
#   8  9  10 11
#   12 13 14 15
CONNECTIONS: Dict[int, Set[int]] = {}
for n in range(16):
    nx = n % 4
    ny = n // 4
    CONNECTIONS[n] = set()
    for m in range(16):
        if n == m:
            # A letter is not connected to itself.
            continue
        mx = m % 4
        my = m // 4
        if not nx - 1 <= mx <= nx + 1:
            continue
        if not ny - 1 <= my <= ny + 1:
            continue
        CONNECTIONS[n].add(m)


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
            f'{self.letters[0:4]}\n'
            f'{self.letters[4:8]}\n'
            f'{self.letters[8:12]}\n'
            f'{self.letters[12:16]}\n'
        )

    def __contains__(self, needle_word: str) -> bool:
        if not needle_word:
            return True

        # needle_word_indexes is a list of lists. Each inner list corresponds
        # to a needle_letter in the needle_world, in order. Each inner list
        # contains the indexes in self.letters where that needle_letter can be
        # found.
        needle_word_indexes: List[List[int]] = []
        for needle_letter in needle_word:
            needle_letter_indexes = []
            for haystack_letter_index, haystack_letter in enumerate(self.letters):  # noqa E501
                match = (
                    needle_letter == haystack_letter or
                    haystack_letter == WILDCARD
                )
                if match:
                    needle_letter_indexes.append(haystack_letter_index)
            if not needle_letter_indexes:
                return False
            needle_word_indexes.append(needle_letter_indexes)

        return self.find_path(needle_word_indexes)

    def find_path(self, needle_word_indexes: List[List[int]]) -> bool:
        stack = [
            (initial_index, 0, [initial_index])
            for initial_index in needle_word_indexes[0]
        ]
        while stack:
            index, depth, path = stack.pop(-1)
            if depth == len(needle_word_indexes) - 1:
                return True
            for next_index in CONNECTIONS[index]:
                if next_index in path:
                    # Do not revisit letters.
                    continue
                if next_index in needle_word_indexes[depth + 1]:
                    stack.append((next_index, depth + 1, path + [next_index]))
        return False

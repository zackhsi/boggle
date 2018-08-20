import random
import uuid
from functools import lru_cache
from typing import Dict, List, Optional, Set

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from boggle.database import Base
from boggle.settings import WILDCARD

# Original UK version (c1976, yellow box)!
# https://gist.github.com/samdobson/6b9a71b39637538338c7e88ced6eb056
DICE = [
    'aaciot', 'abilty', 'abjmoq', 'acdemp', 'acelrs', 'adenvz', 'ahmors',
    'biforx', 'denosw', 'dknotu', 'eefhiy', 'egkluy', 'egintv', 'ehinps',
    'elpstu', 'gilruw',
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


@lru_cache(maxsize=None)
class BoardNode:
    def __init__(
        self,
        *,
        index: int,
        letters: List[str],
    ) -> None:
        self.index = index
        self.letters = letters

    def children(self) -> List:
        return [
            BoardNode(
                index=index,
                letters=self.letters,
            )
            for index in CONNECTIONS[self.index]
        ]

    @property
    def letter(self) -> str:
        return self.letters[self.index]


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

    def compare_letters(self, a: str, b: str) -> bool:
        if a == WILDCARD or b == WILDCARD:
            return True
        return a == b

    def __contains__(self, needle_word: str) -> bool:
        """
        Detect if a word is in the board, subject to wildcard logic.

        At a high level, this method performs a DFS of the board. The DFS stack
        is initially seeded with nodes representing matches of the first letter
        of the needle word.
        """
        if not needle_word:
            return True

        stack = []
        for haystack_letter_index, haystack_letter in enumerate(self.letters):
            if self.compare_letters(haystack_letter, needle_word[0]):
                node = BoardNode(
                    index=haystack_letter_index,
                    letters=self.letters,
                )
                # node, depth, path.
                stack.append((node, 0, [node]))

        while stack:
            node, depth, path = stack.pop(-1)
            if depth == len(needle_word) - 1:
                return True
            for child in node.children():
                # Do not revisit.
                if child in path:
                    continue
                if self.compare_letters(child.letter, needle_word[depth + 1]):
                    stack.append((child, depth + 1, path + [child]))

        return False

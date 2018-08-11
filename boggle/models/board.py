import random
from typing import Optional


class Board:
    # Original UK version (c1976, yellow box)!
    # https://gist.github.com/samdobson/6b9a71b39637538338c7e88ced6eb056
    DICE = [
        'AACIOT', 'ABILTY', 'ABJMOQ', 'ACDEMP', 'ACELRS', 'ADENVZ', 'AHMORS',
        'BIFORX', 'DENOSW', 'DKNOTU', 'EEFHIY', 'EGKLUY', 'EGINTV', 'EHINPS',
        'ELPSTU', 'GILRUW',
    ]

    def __init__(self, board_string: Optional[str] = None) -> None:
        if board_string:
            letters = board_string.split(', ')
            if len(letters) != 16:
                raise ValueError('Board requires 16 letters')
        else:
            letters = [random.choice(die) for die in self.DICE]
        self.board = [
            letters[0:4],
            letters[4:8],
            letters[8:12],
            letters[12:16],
        ]

    def __str__(self) -> str:
        row_strings = []
        for row in self.board:
            row_strings.append(' '.join(row))
        return '\n'.join(row_strings)

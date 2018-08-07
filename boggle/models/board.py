class Board:
    def __init__(self, board_string: str) -> None:
        letters = board_string.split(', ')
        if len(letters) != 16:
            raise ValueError('Board requires 16 letters')
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

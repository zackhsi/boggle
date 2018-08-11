from typing import Optional

import pytest

from boggle.models.board import Board


@pytest.mark.parametrize(
    ('board_string'),
    [
        'T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D',
        None,
    ]
)
def test_board_valid(board_string: Optional[str]) -> None:
    assert Board(board_string)


def test_board_invalid() -> None:
    board_string = 'T, A, P, *, E, A, K, S, O, B, R, S, S, *, X'
    with pytest.raises(ValueError):
        Board(board_string)

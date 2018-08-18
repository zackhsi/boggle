import textwrap
from typing import Optional

import pytest

from boggle.models.board import Board


@pytest.mark.parametrize(
    ('board_string', 'valid'),
    [
        ('T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D', True),
        (None, True),
        # Not enough letters.
        ('T, A, P, *, E, A', False),
        # Too many letters.
        ('T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D, X', False),
    ]
)
def test_create(board_string: Optional[str], valid: bool) -> None:
    if valid:
        assert Board(board_string)
    else:
        with pytest.raises(ValueError):
            Board(board_string)


@pytest.fixture
def board_no_wilds() -> Board:
    board_string = 'A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P'
    board = Board(board_string)
    expected_string = textwrap.dedent(
        """\
        ABCD
        EFGH
        IJKL
        MNOP
        """
    )
    assert str(board) == expected_string
    return board


@pytest.mark.parametrize(
    ('needle_word', 'expected_result'),
    [
        ('', True),
        ('ABCD', True),  # Horizontal.
        ('AEIM', True),  # Vertical.
        ('AFKP', True),  # Diagonal.
        ('ABCGKONMIE', True),  # Square.
        ('AC', False),  # Disconnected.
        ('ABFEA', False),  # Revisit.
    ]
)
def test_contains_no_wilds(
    board_no_wilds: Board,
    needle_word: str,
    expected_result: bool
) -> None:
    if expected_result:
        assert needle_word in board_no_wilds
    else:
        assert needle_word not in board_no_wilds


@pytest.fixture
def board_with_wilds() -> Board:
    board_string = 'A, B, C, D, E, *, G, H, I, J, *, L, M, N, O, P'
    board = Board(board_string)
    expected_string = textwrap.dedent(
        """\
        ABCD
        E*GH
        IJ*L
        MNOP
        """
    )
    assert str(board) == expected_string
    return board


@pytest.mark.parametrize(
    ('needle_word', 'expected_result'),
    [
        ('EFGH', True),
        ('EXGH', True),
        ('XGXJ', True),
        ('BXXJX', False),
    ]
)
def test_contains_with_wilds(
    board_with_wilds: Board,
    needle_word: str,
    expected_result: bool
) -> None:
    if expected_result:
        assert needle_word in board_with_wilds
    else:
        assert needle_word not in board_with_wilds

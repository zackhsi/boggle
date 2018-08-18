import pytest
from aiohttp.test_utils import TestClient as _TestClient
from pytest_mock import MockFixture

from boggle import dictionary
from boggle.models.board import Board
from boggle.settings import (
    REASON_NOT_IN_BOARD_FMT,
    REASON_NOT_IN_DICTIONARY_FMT,
)


@pytest.mark.parametrize(
    (
        'word',
        'mock_board_contains',
        'mock_dictionary_lookup',
        'expected_status',
        'expected_404_reason',
    ),
    [
        ('testword', True, True, 204, ''),
        ('testword', True, False, 404, REASON_NOT_IN_DICTIONARY_FMT),
        ('testword', False, True, 404, REASON_NOT_IN_BOARD_FMT),
        # For invalid words that are also not in the board, return that the
        # word is invalid.
        ('testword', False, False, 404, REASON_NOT_IN_DICTIONARY_FMT),
        ('oversixteenletters', True, True, 400, ''),
    ]
)
async def test_gamewords(
    mocker: MockFixture,
    client: _TestClient,
    game_id_started: str,
    word: str,
    mock_board_contains: bool,
    mock_dictionary_lookup: bool,
    expected_status: int,
    expected_404_reason: str,
) -> None:
    mocker.patch.object(
        Board,
        '__contains__',
        return_value=mock_board_contains,
    )
    mocker.patch.object(
        dictionary,
        'lookup',
        return_value=mock_dictionary_lookup,
    )
    response = await client.post(
        f'/games/{game_id_started}/words',
        json={'word': word},
    )
    assert response.status == expected_status
    if expected_status == 404:
        data = await response.json()
        reason = data['reason']
        assert reason == expected_404_reason.format(word=word)

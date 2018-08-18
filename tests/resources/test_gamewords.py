import pytest
from aiohttp.test_utils import TestClient as _TestClient
from pytest_mock import MockFixture

from boggle.models.board import Board


@pytest.mark.parametrize(
    ('word', 'mock_contains', 'expected_status'),
    [
        ('', False, 400),
        ('oversixteenletters', True, 400),
        ('abcd', False, 404),
        ('abcd', True, 204),
    ]
)
async def test_gamewords(
    mocker: MockFixture,
    client: _TestClient,
    game_id_started: str,
    word: str,
    mock_contains: bool,
    expected_status: int,
) -> None:
    mocker.patch.object(
        Board,
        '__contains__',
        return_value=mock_contains
    )
    response = await client.post(
        f'/games/{game_id_started}/words',
        json={'word': word},
    )
    assert response.status == expected_status

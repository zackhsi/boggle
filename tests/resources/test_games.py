from typing import Dict

import pytest
from aiohttp.test_utils import TestClient as _TestClient


@pytest.fixture
async def game_data(client: _TestClient) -> Dict:
    response = await client.post('/games')
    assert response.status == 200
    data: Dict = await response.json()
    return data


@pytest.fixture
async def game_id_created(game_data: Dict) -> str:
    game_id: str = game_data['id']
    return game_id


@pytest.fixture
async def game_id_started(
    client: _TestClient,
    game_id_created: str,
) -> str:
    response = await client.put(
        f'/games/{game_id_created}',
        json={
            'started': True,
        }
    )
    game = await response.json()
    assert game['started_at']
    return game_id_created


async def test_get_empty(client: _TestClient) -> None:
    response = await client.get('/games')
    assert response.status == 200
    data = await response.json()
    games = data['games']
    assert games == []


async def test_get_started_game(
    client: _TestClient,
    game_id_started: str,
) -> None:
    response = await client.get(
        f'/games',
        params={'id': game_id_started}
    )
    data = await response.json()
    game = data['games'][0]
    assert game['started_at']
    assert game['board']['letters']


async def test_post(client: _TestClient) -> None:
    response = await client.post('/games')
    assert response.status == 200
    game = await response.json()
    game_id = game['id']
    response = await client.get('/games')
    data = await response.json()
    games = data['games']
    game_ids = [g['id'] for g in games]
    assert game_id in game_ids

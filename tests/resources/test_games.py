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
async def game_id(game_data: Dict) -> str:
    game_id: str = game_data['id']
    return game_id


async def test_get(client: _TestClient) -> None:
    response = await client.get('/games')
    assert response.status == 200
    data = await response.json()
    games = data['games']
    assert games == []


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


async def test_put(
    client: _TestClient,
    game_id: str,
) -> None:
    response = await client.put(
        f'/games/{game_id}',
        json={
            'started': True,
        }
    )
    game = await response.json()
    assert game['started_at']

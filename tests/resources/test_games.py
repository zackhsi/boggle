from aiohttp.test_utils import TestClient as _TestClient


async def test_get(client: _TestClient) -> None:
    response = await client.get('/games')
    assert response.status == 200
    games = await response.json()
    assert games == []


async def test_post(client: _TestClient) -> None:
    response = await client.post('/games')
    assert response.status == 200
    response = await response.json()
    game_id = response['id']
    response = await client.get('/games')
    assert response.status == 200
    games = await response.json()
    assert game_id in games

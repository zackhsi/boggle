from typing import Callable, Dict, Generator

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from boggle import models
from boggle.database import Base
from boggle.server import create_application
from boggle.settings import ENVIRONMENT, TESTING

if ENVIRONMENT != TESTING:
    raise RuntimeError(f'Tests can only run if ENVIRONMENT={TESTING}!')


@pytest.fixture
def tables() -> Generator:
    models.load()
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture
async def application() -> web.Application:
    application = create_application()
    yield application
    await application.shutdown()


@pytest.fixture
async def client(
    application: web.Application,
    aiohttp_client: Callable,
    tables: None,
) -> TestClient:
    yield await aiohttp_client(application)


@pytest.fixture
async def game_data(client: TestClient) -> Dict:
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
    client: TestClient,
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

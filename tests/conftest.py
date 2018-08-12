from typing import Callable, Generator

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
    return create_application()


@pytest.fixture
async def client(
    application: web.Application,
    aiohttp_client: Callable,
    tables: None,
) -> TestClient:
    return await aiohttp_client(application)

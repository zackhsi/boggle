import logging
from typing import Callable

from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from boggle.settings import DB_CONNECTION_STRING

logger = logging.getLogger(__name__)

engine = create_engine(DB_CONNECTION_STRING)
Base = declarative_base(bind=engine)
SessionMaker = sessionmaker(bind=engine)


async def session_middleware(
    _: web.Application,
    handler: Callable[[web.Request, Session], web.Response],
) -> Callable:
    async def middleware_handler(request: web.Request) -> web.Response:
        session = SessionMaker()
        response = await handler(request, session)
        try:
            session.commit()
        except Exception:
            logger.exception('Failed to commit session, rolling back...')
            session.rollback()
        finally:
            session.close()
        return response

    return middleware_handler

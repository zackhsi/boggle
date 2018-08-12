import logging
from typing import Callable

from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from boggle.settings import DB_URI, POSTGRES_URI

logger = logging.getLogger(__name__)

cluster_engine = create_engine(POSTGRES_URI)
database_engine = create_engine(DB_URI)
Base = declarative_base(bind=database_engine)
SessionMaker = sessionmaker(bind=database_engine)


async def session_middleware(
    _: web.Application,
    handler: Callable[[web.Request], web.Response],
) -> Callable:
    async def middleware_handler(request: web.Request) -> web.Response:
        session: Session = SessionMaker()
        request.session = session
        response = await handler(request)
        try:
            session.commit()
        except Exception:
            logger.exception('Failed to commit session, rolling back...')
            session.rollback()
        finally:
            session.close()
        return response

    return middleware_handler

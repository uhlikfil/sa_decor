import pytest
import pytest_asyncio
from _db_mock.dbschema import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite://")


@pytest.fixture(scope="module")
def async_engine():
    return create_async_engine("sqlite+aiosqlite://")


@pytest.fixture(scope="module")
def session_maker(engine):
    return sessionmaker(engine, autocommit=False)


@pytest.fixture(scope="module")
def async_session_maker(async_engine):
    return sessionmaker(async_engine, autocommit=False, class_=AsyncSession)


@pytest.fixture(scope="module", autouse=True)
def setup_db(engine):
    Base.metadata.create_all(engine)


@pytest_asyncio.fixture(autouse=True)
async def setup_async_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

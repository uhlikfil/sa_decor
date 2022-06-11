import pytest
from _db_mock.async_engine_queries import create_person, get_persons

from sa_decor import set_global_engine


@pytest.fixture(scope="module", autouse=True)
def set_up_async(async_engine):
    set_global_engine(async_engine)


@pytest.mark.asyncio
async def test_async_no_connection():
    r = await create_person("Karel Barel", 35)
    assert r.rowcount == 1


@pytest.mark.asyncio
async def test_async_existing_connection(async_engine):
    async with async_engine.connect() as conn:
        await create_person("Jean Tomato", 27, connection=conn)
        await create_person("Karel Tomato", 21, connection=conn)
        r = await get_persons("Tomato", connection=conn)
        assert len(r) == 2

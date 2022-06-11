import pytest
from _db_mock.async_session_queries import (
    create_person,
    create_person_with_err,
    create_person_with_err_non_commit,
    get_persons,
)

from sa_decor import set_global_sessionmaker


@pytest.fixture(scope="module", autouse=True)
def set_up_async(async_session_maker):
    set_global_sessionmaker(async_session_maker)


@pytest.mark.asyncio
async def test_async_no_session():
    r = await create_person("Karel Barel", 35)
    assert r.rowcount == 1


@pytest.mark.asyncio
async def test_async_existing_session(async_session_maker):
    async with async_session_maker() as sess:
        await create_person("Jean Tomato", 27, session=sess)
        await create_person("Karel Tomato", 21, session=sess)
        r = await get_persons("Tomato", session=sess)
        assert len(r) == 2


@pytest.mark.asyncio
async def test_force_commit_enabled():
    try:
        await create_person_with_err("Karel Barel", 28)
    except Exception:
        pass
    r = await get_persons("Barel")
    assert len(r) > 0


@pytest.mark.asyncio
async def test_force_commit_disabled():
    try:
        await create_person_with_err_non_commit("Karel Varel", 29)
    except Exception:
        pass
    r = await get_persons("Varel")
    assert len(r) == 0

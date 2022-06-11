from _db_mock.dbschema import Person
from sqlalchemy import insert, select

from sa_decor.asyncio import with_async_session


@with_async_session(commit=True)
async def create_person(name: str, age: int, *, session):
    firstname, lastname = name.split(maxsplit=1)
    stmt = insert(Person).values(firstname=firstname, lastname=lastname, age=age)
    return await session.execute(stmt)


@with_async_session(commit=False)
async def get_persons(lastname: str, *, session) -> list[Person]:
    stmt = select(Person).where(Person.lastname == lastname)
    return list(await session.execute(stmt))


@with_async_session(force_commit=True)
async def create_person_with_err(name: str, age: int, *, session):
    await create_person(name, age, session)
    raise Exception


@with_async_session(force_commit=False)
async def create_person_with_err_non_commit(name: str, age: int, *, session):
    await create_person(name, age, session=session)
    raise Exception

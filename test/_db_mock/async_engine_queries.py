from _db_mock.dbschema import Person
from sqlalchemy import insert, select

from sa_decor.asyncio import with_async_connection


@with_async_connection()
async def create_person(name: str, age: int, *, connection):
    firstname, lastname = name.split(maxsplit=1)
    stmt = insert(Person).values(firstname=firstname, lastname=lastname, age=age)
    return await connection.execute(stmt)


@with_async_connection()
async def get_persons(lastname: str, *, connection) -> list[Person]:
    stmt = select(Person).where(Person.lastname == lastname)
    return list(await connection.execute(stmt))

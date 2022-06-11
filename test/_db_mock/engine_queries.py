from _db_mock.dbschema import Person
from sqlalchemy import insert, select

from sa_decor import with_connection


@with_connection()
def create_person(name: str, age: int, *, connection):
    firstname, lastname = name.split(maxsplit=1)
    stmt = insert(Person).values(firstname=firstname, lastname=lastname, age=age)
    return connection.execute(stmt)


@with_connection()
def get_persons(lastname: str, *, connection) -> list[Person]:
    stmt = select(Person).where(Person.lastname == lastname)
    return list(connection.execute(stmt))

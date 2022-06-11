from _db_mock.dbschema import Person
from sqlalchemy import insert, select

from sa_decor import with_session


@with_session(commit=True)
def create_person(name: str, age: int, *, session):
    firstname, lastname = name.split(maxsplit=1)
    stmt = insert(Person).values(firstname=firstname, lastname=lastname, age=age)
    return session.execute(stmt)


@with_session(commit=False)
def get_persons(lastname: str, *, session) -> list[Person]:
    stmt = select(Person).where(Person.lastname == lastname)
    return list(session.execute(stmt))


@with_session(force_commit=True)
def create_person_with_err(name: str, age: int, *, session):
    create_person(name, age, session=session)
    raise Exception


@with_session(force_commit=False)
def create_person_with_err_non_commit(name: str, age: int, *, session):
    create_person(name, age, session=session)
    raise Exception

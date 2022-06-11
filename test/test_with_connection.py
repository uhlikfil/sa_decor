import pytest
from _db_mock.engine_queries import create_person, get_persons

from sa_decor import set_global_engine


@pytest.fixture(scope="module", autouse=True)
def set_up_async(engine):
    set_global_engine(engine)


def test_no_connection():
    r = create_person("Filip C", 24)
    assert r.rowcount == 1


def test_existing_connection(engine):
    with engine.connect() as conn:
        create_person("Jean Tomato", 27, connection=conn)
        create_person("Karel Tomato", 21, connection=conn)
        r = get_persons("Tomato", connection=conn)
        assert len(r) == 2

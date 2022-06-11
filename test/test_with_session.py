import pytest
from _db_mock.session_queries import (
    create_person,
    create_person_with_err,
    create_person_with_err_non_commit,
    get_persons,
)

from sa_decor import set_global_sessionmaker


@pytest.fixture(scope="module", autouse=True)
def set_up_async(session_maker):
    set_global_sessionmaker(session_maker)


def test_no_session():
    r = create_person("Filip C", 24)
    assert r.rowcount == 1


def test_existing_session(session_maker):
    with session_maker() as sess:
        create_person("Jean Tomato", 27, session=sess)
        create_person("Karel Tomato", 21, session=sess)
        r = get_persons("Tomato", session=sess)
        assert len(r) == 2


def test_force_commit_enabled():
    try:
        create_person_with_err("Karel Barel", 28)
    except Exception:
        pass
    r = get_persons("Barel")
    assert len(r) > 0


def test_force_commit_disabled():
    try:
        create_person_with_err_non_commit("Karel Varel", 29)
    except Exception:
        pass
    r = get_persons("Varel")
    assert len(r) == 0

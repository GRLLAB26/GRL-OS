from app import crud
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def setup_temp_db(tmp_path):
    db_file = tmp_path / "crud.db"
    url = f"sqlite:///{db_file}"
    engine = create_engine(url, future=True)
    Base.metadata.create_all(bind=engine)
    # override app.db engine/session for this test by monkeypatching crud.get_session
    return url


def test_crud_lifecycle(tmp_path, monkeypatch):
    url = setup_temp_db(tmp_path)

    # patch get_session to use this DB
    from app import db

    engine = create_engine(url, future=True)
    Session = sessionmaker(bind=engine, future=True)

    def session_ctx():
        s = Session()
        try:
            yield s
            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()

    # monkeypatch the get_session contextmanager
    monkeypatch.setattr(db, "SessionLocal", Session)

    # Create
    u = crud.create_user("Test", "test@example.com")
    assert u.id is not None

    # List
    users = crud.list_users()
    assert any(x.email == "test@example.com" for x in users)

    # Update
    u2 = crud.update_user(u.id, "Test2", "test2@example.com")
    assert u2 is not None
    assert u2.name == "Test2"

    # Get
    got = crud.get_user(u.id)
    assert got.email == "test2@example.com"

    # Delete
    ok = crud.delete_user(u.id)
    assert ok
    assert crud.get_user(u.id) is None

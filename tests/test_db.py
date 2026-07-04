import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models import User, Base


def test_create_user(tmp_path):
    db_file = tmp_path / "test.db"
    url = f"sqlite:///{db_file}"

    engine = create_engine(url, future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, future=True)

    with Session() as s:
        user = User(name="Alice", email="alice@example.com")
        s.add(user)
        s.commit()
        s.refresh(user)
        assert user.id is not None

        result = s.execute(text("SELECT count(*) FROM users")).scalar()
        assert result == 1

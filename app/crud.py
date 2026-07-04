from typing import List, Optional

from sqlalchemy import select

from .db import get_session
from .models import User


def create_user(name: str, email: str) -> User:
    with get_session() as s:
        user = User(name=name, email=email)
        s.add(user)
        s.refresh(user)
        return user


def list_users() -> List[User]:
    with get_session() as s:
        return s.query(User).order_by(User.id).all()


def get_user(user_id: int) -> Optional[User]:
    with get_session() as s:
        return s.get(User, user_id)


def delete_user(user_id: int) -> bool:
    with get_session() as s:
        u = s.get(User, user_id)
        if not u:
            return False
        s.delete(u)
        return True


def update_user(user_id: int, name: str, email: str) -> Optional[User]:
    with get_session() as s:
        u = s.get(User, user_id)
        if not u:
            return None
        u.name = name
        u.email = email
        s.add(u)
        s.refresh(u)
        return u

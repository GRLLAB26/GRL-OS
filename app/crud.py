from typing import List, Optional
from dataclasses import dataclass

from sqlalchemy import select

from .db import get_session
from .models import User
@dataclass
class UserOut:
    id: int
    name: str
    email: str


def create_user(name: str, email: str) -> User:
    with get_session() as s:
        user = User(name=name, email=email)
        s.add(user)
        s.flush()
        s.refresh(user)
        return UserOut(id=user.id, name=user.name, email=user.email)


def list_users() -> List[User]:
    with get_session() as s:
        rows = s.query(User).order_by(User.id).all()
        return [UserOut(id=r.id, name=r.name, email=r.email) for r in rows]


def get_user(user_id: int) -> Optional[UserOut]:
    with get_session() as s:
        r = s.get(User, user_id)
        if not r:
            return None
        return UserOut(id=r.id, name=r.name, email=r.email)


def delete_user(user_id: int) -> bool:
    with get_session() as s:
        u = s.get(User, user_id)
        if not u:
            return False
        s.delete(u)
        return True


def update_user(user_id: int, name: str, email: str) -> Optional[UserOut]:
    with get_session() as s:
        u = s.get(User, user_id)
        if not u:
            return None
        u.name = name
        u.email = email
        s.add(u)
        s.flush()
        s.refresh(u)
        return UserOut(id=u.id, name=u.name, email=u.email)

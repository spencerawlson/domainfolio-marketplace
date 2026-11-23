"""Shared FastAPI dependencies (auth context, DB session).

P0 skeleton: `get_db` yields a session; `get_current_user` is a stub
that returns None until the auth stage lands real session/JWT auth.
Routers must not invent their own auth — they use these deps.
"""

from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_session_factory


def get_db() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def get_current_user(_db: Session = Depends(get_db)):
    """Placeholder until the P0 auth stage. Returns None and must never
    be treated as an authenticated identity by any router."""
    return None

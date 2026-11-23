"""Declarative base for all marketplace models. Every model lives in its
own module's models.py and is imported by alembic/env.py; nothing is
defined here besides the base."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

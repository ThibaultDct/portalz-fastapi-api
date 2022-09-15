from dataclasses import dataclass
from datetime import datetime
import string
import uuid as uuid_pkg
from pydantic import BaseModel
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlmodel import SQLModel, Column, DateTime, Field

class User(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username: str
    email: str
    created_at: datetime = datetime.now()
    is_active: bool = True
    password: str

class UserDto(SQLModel, table=False):
    username: str
    password: str
    email: str
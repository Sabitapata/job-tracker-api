from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    email: str = Field(index=True, unique=True)
    hashed_password: str


class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)

    company: str
    role: str
    status: str = "Applied"
    notes: Optional[str] = None
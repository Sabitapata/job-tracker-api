from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfileUpdate(BaseModel):
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None


class JobApplicationOut(BaseModel):
    id: int
    user_id: int
    company: str
    role: str
    status: Literal["Applied", "Interview", "Offer", "Rejected"]
    notes: Optional[str] = None


class JobApplicationCreate(BaseModel):
    company: str = Field(min_length=2, max_length=100)
    role: str = Field(min_length=2, max_length=100)
    status: Literal["Applied", "Interview", "Offer", "Rejected"] = "Applied"
    notes: Optional[str] = Field(default=None, max_length=1000)


class JobApplicationUpdate(BaseModel):
    company: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role: Optional[str] = Field(default=None, min_length=2, max_length=100)
    status: Optional[
        Literal["Applied", "Interview", "Offer", "Rejected"]
    ] = None
    notes: Optional[str] = Field(default=None, max_length=1000)
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

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
    notes: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    company: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role: Optional[str] = Field(default=None, min_length=2, max_length=100)
    status: Optional[
        Literal["Applied", "Interview", "Offer", "Rejected"]
    ] = None
    notes: Optional[str] = None
"""Post schemas"""
from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    """Base post scheme"""
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """Scheme for creating new post"""
    pass


class Post(PostBase):
    """Scheme for response as post"""
    id: int
    created_at: datetime

    class Config:
        """Also trying to get information as attribute (id = data.id)"""
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Scheme for response to new user creation"""
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """Also trying to get information as attribute (id = data.id)"""
        orm_mode = True

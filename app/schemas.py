"""Post schemas

Basic validations of
what user can get and send as request
"""
from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Scheme for creating new user"""
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
    owner: UserResponse

    class Config:
        """Also trying to get information as attribute (id = data.id)"""
        orm_mode = True


class PostResponse(BaseModel):
    Post: Post
    likes: int

    class Config:
        """Also trying to get information as attribute (id = data.id)"""
        orm_mode = True


class Token(BaseModel):
    """Response JWT scheme"""
    token: str
    token_type: str


class TokenData(BaseModel):
    """Scheme for token that verify user rights"""
    user_id: Optional[str] = None


class Rate(BaseModel):
    post_id: int
    dir: Literal[0, 1]  # direction: 0 - remove, 1 - add

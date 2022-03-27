"""Post schemas"""
from pydantic import BaseModel


class PostBase(BaseModel):
    """Base post scheme"""
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """Scheme for creating new post"""
    pass

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


my_posts = [{"title": "post1", "content": "post1 content", "id": 1},
            {"title": "post2", "content": "post2 content", "id": 2}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hi :)"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict: dict = dict(post)
    post_dict["id"] = randrange(1000)
    my_posts.append(post_dict)
    return {"new post": f"title: {post_dict}"}

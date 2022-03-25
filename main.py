from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

# TODO documentation, header
app = FastAPI()

all_posts = [{"title": "post1", "content": "post1 content", "id": 1},
             {"title": "post2", "content": "post2 content", "id": 2}]


def find_by_id(id_: int) -> dict | None:
    for post in all_posts:
        if post["id"] == id_:
            return post
    return None

def find_post_index(id_: int) -> int | None:
    for index, post in enumerate(all_posts):
        if post["id"] == id_:
            return index
    return None


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
    return {"data": all_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict: dict = dict(post)
    post_dict["id"] = randrange(1000)
    all_posts.append(post_dict)
    return {"new post": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    return {"post_detail": all_posts[-1]}


@app.get("/posts/{id_}")
def get_post(id_: int):
    post = find_by_id(id_)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return {"post_detail": post}


@app.delete("/posts/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int):
    post_index = find_post_index(id_)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    all_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id_}")
def update_post(id_: int, post: Post):
    post_index = find_post_index(id_)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    post_dict = dict(post)
    post_dict["id"] = id_
    all_posts[post_index] = post_dict
    return {"post_detail": post_dict}

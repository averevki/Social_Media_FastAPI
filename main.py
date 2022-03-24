from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"message": "you"}


@app.post("/createpost")
def create_post(new_post: Post):
    # print(payload)
    return {"new post": f"title: {new_post.title} content: {new_post.content}"}

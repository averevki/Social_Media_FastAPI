from random import randrange
from time import sleep

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# TODO documentation, header
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="social_media_db", user="postgres", password="2682",
                                cursor_factory=RealDictCursor)  # TODO move information into .env
        cur = conn.cursor()
        print("Successful database connection")
        break
    except Exception as e:
        print(f"Database connection failed.\nError: {e}")
        sleep(2)
        print("Trying again...")


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Hi :)"}


@app.get("/posts")
def get_posts():
    # fetch all existing posts
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return {"all posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # insert single raw, avoiding SQL injections by inserting without f-string
    cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                (post.title, post.content, post.published))
    # get created post for returning
    created_post = cur.fetchone()
    # commit changes into database
    conn.commit()
    return {"new post": created_post}


@app.get("/posts/latest")
def get_latest_post():
    # get last row from posts
    cur.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    latest_post = cur.fetchone()
    return {"latest post": latest_post}


@app.get("/posts/{id_}")
def get_post(id_: int):
    # find post by id, avoiding SQL injections by inserting without f-string
    cur.execute("SELECT * FROM posts WHERE id = %s", str(id_))
    found_post = cur.fetchone()
    # return 404 if post was not found
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return {"found post": found_post}


@app.delete("/posts/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int):
    # delete post by id, avoiding SQL injections by inserting without f-string
    cur.execute("DELETE FROM posts WHERE id = %s RETURNING *", str(id_))
    deleted_post = cur.fetchone()
    # commit changes into database
    conn.commit()
    # return 404 if post was not found
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id_}")
def update_post(id_: int, post: Post):
    # updated post by id, avoiding SQL injections by inserting without f-string
    cur.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                (post.title, post.content, post.published, str(id_)))
    updated_post = cur.fetchone()
    # commit database changes
    conn.commit()
    # return 404 if post was not found
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return {"updated post": updated_post}

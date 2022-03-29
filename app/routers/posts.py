from fastapi import Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .. import models, schemas
from ..main import app


@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # fetch all existing posts
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # insert single post
    created_post = models.Post(**dict(post))    # unpack class as dictionary for easier input
    db.add(created_post)
    # commit changes into database
    db.commit()
    # get created post for returning
    db.refresh(created_post)
    return created_post


@app.get("/posts/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db)):
    # get last inserted post
    latest_post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    return latest_post


@app.get("/posts/{id_}", response_model=schemas.Post)
def get_post(id_: int, db: Session = Depends(get_db)):
    # find post by id
    found_post = db.query(models.Post).filter(models.Post.id == id_).first()
    # return 404 if post was not found
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return found_post


@app.delete("/posts/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int, db: Session = Depends(get_db)):
    # find post for deletion by id
    deleted_post = db.query(models.Post).filter(models.Post.id == id_)
    # return 404 if post was not found
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    # if deleted post exist - delete
    deleted_post.delete(synchronize_session=False)
    # commit changes into database
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id_}", response_model=schemas.Post)
def update_post(id_: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # find post by id
    updated_post = db.query(models.Post).filter_by(id=id_)
    # return 404 if post was not found
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    # if updated post exist, update it
    updated_post.update(dict(post), synchronize_session=False)
    # commit database changes
    db.commit()
    return updated_post.first()

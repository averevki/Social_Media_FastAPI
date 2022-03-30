"""Router with post queries"""
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .. import models, schemas, oauth2
from ..database import get_db

# define router
router = APIRouter()


@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)) -> list[schemas.Post]:
    # fetch all existing posts
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                verify_user: models.User = Depends(oauth2.verify_current_user)) -> schemas.Post:
    # insert single post
    created_post = models.Post(**dict(post), owner_id=verify_user.id)      # unpack class as dict for easier input
    db.add(created_post)
    # commit changes into database
    db.commit()
    # get created post for returning
    db.refresh(created_post)
    return created_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db)) -> schemas.Post:
    # get last inserted post
    latest_post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    return latest_post


@router.get("/{id_}", response_model=schemas.Post)
def get_post(id_: int, db: Session = Depends(get_db)) -> schemas.Post:
    # find post by id
    found_post = db.query(models.Post).filter(models.Post.id == id_).first()
    # return 404 if post was not found
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return found_post


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int, db: Session = Depends(get_db),
                verify_user: int = Depends(oauth2.verify_current_user)):
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


@router.put("/{id_}", response_model=schemas.Post)
def update_post(id_: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                verify_user: int = Depends(oauth2.verify_current_user)) -> schemas.Post:
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

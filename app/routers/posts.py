"""Router with post queries"""
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from .. import database, models, schemas, oauth2

# declare router
router = APIRouter()


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(database.get_db),
              limit: int = 10, skip: int = 0, search: str = "") -> list[schemas.PostResponse]:
    # fetch all existing, published posts
    posts = db.query(models.Post, func.count(models.Rating.post_id).label("likes"))\
        .join(models.Rating, models.Rating.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search), models.Post.published == "TRUE")\
        .order_by(desc(models.Post.created_at))\
        .limit(limit).offset(skip).all()
    return posts


@router.get("/my", response_model=list[schemas.PostResponse])
def get_posts_my(db: Session = Depends(database.get_db),
                 verified_user: models.User = Depends(oauth2.verify_current_user),
                 limit: int = 10, skip: int = 0, search: str = "") -> list[schemas.PostResponse]:
    # fetch all user posts
    posts = db.query(models.Post, func.count(models.Rating.post_id).label("likes"))\
        .join(models.Rating, models.Rating.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search), models.Post.owner_id == verified_user.id)\
        .order_by(desc(models.Post.created_at))\
        .limit(limit).offset(skip).all()
    return posts


@router.get("/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(database.get_db)) -> schemas.PostResponse:
    # get last posted
    latest_post = db.query(models.Post, func.count(models.Rating.post_id).label("likes"))\
        .join(models.Rating, models.Rating.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.published == "TRUE")\
        .order_by(desc(models.Post.created_at)).first()
    return latest_post


@router.get("/{id_}", response_model=schemas.PostResponse)
def get_post(id_: int, db: Session = Depends(database.get_db),
             verified_user: models.User = Depends(oauth2.verify_current_user)) -> schemas.PostResponse:
    # find post by id
    found_post = db.query(models.Post, func.count(models.Rating.post_id).label("likes"))\
        .join(models.Rating, models.Rating.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id_).first()
    # return 404 if post was not found
    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    # return 404 if getting not published post from another user
    if found_post.Post.published is False and found_post.Post.owner_id != verified_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    return found_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db),
                verified_user: models.User = Depends(oauth2.verify_current_user)) -> schemas.Post:
    # insert single post
    created_post = models.Post(**dict(post), owner_id=verified_user.id)      # unpack class as dict for easier input
    db.add(created_post)
    # commit changes into database
    db.commit()
    # get created post for returning
    db.refresh(created_post)
    return created_post


@router.put("/publish/{id_}")
def change_post_visibility(id_: int, db: Session = Depends(database.get_db),
                           verified_user: models.User = Depends(oauth2.verify_current_user)):
    # find post by id
    post = db.query(models.Post).filter(models.Post.id == id_)
    fetched_post = post.first()
    # raise 404 if post wasn't found
    if fetched_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    # raise 403 if user have insufficient rights
    if fetched_post.owner_id != verified_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="unauthorized action")
    # fetched_post.published = not fetched_post.published
    updated_post = schemas.PostCreate(title=fetched_post.title, content=fetched_post.content,
                                      published=not fetched_post.published)
    # update fetched post
    post.update(dict(updated_post), synchronize_session=False)
    # commit changes into the database
    db.commit()
    return {"detail": f"post was successfully {'' if updated_post.published else 'un'}published (id: {id_})"}


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int, db: Session = Depends(database.get_db),
                verified_user: models.User = Depends(oauth2.verify_current_user)):
    # find post for deletion by id
    deleted_post = db.query(models.Post).filter(models.Post.id == id_)
    post = deleted_post.first()
    # return 404 if post was not found
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    # return 403 if post isn't owned by user
    if post.owner_id != verified_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="unauthorized action")
    # if deleted post exist - delete
    deleted_post.delete(synchronize_session=False)
    # commit changes into database
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id_}", response_model=schemas.PostResponse)
def update_post(id_: int, post: schemas.PostCreate, db: Session = Depends(database.get_db),
                verified_user: models.User = Depends(oauth2.verify_current_user)) -> schemas.PostResponse:
    # find post by id
    updated_post = db.query(models.Post).filter_by(id=id_)
    fetched_post = updated_post.first()
    # return 404 if post was not found
    if fetched_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {id_})")
    if fetched_post.owner_id != verified_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="unauthorized action")
    # if updated post exist, update it
    updated_post.update(dict(post), synchronize_session=False)
    # commit database changes
    db.commit()
    # fetch updated post for respond
    updated_post = db.query(models.Post, func.count(models.Rating.post_id).label("likes"))\
        .join(models.Rating, models.Rating.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id_).first()
    return updated_post

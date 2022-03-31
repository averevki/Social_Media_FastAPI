"""Router with voting queries"""
from typing import Optional

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def rate_post(rate: schemas.Rate, db: Session = Depends(database.get_db),
              verified_user: models.User = Depends(oauth2.verify_current_user)) -> dict:
    # firstly check if post exist and user have sufficient rights
    post: Optional[models.Post] = db.query(models.Post)\
        .filter(models.Post.id == rate.post_id, models.Post.published == "TRUE").first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post was not found (id: {rate.post_id})")
    if post.owner_id == verified_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you can't rate your own post")
    # found rating
    rating = db.query(models.Rating)\
        .filter(models.Rating.post_id == rate.post_id, models.Rating.user_id == verified_user.id)
    vote: Optional[models.Rating] = rating.first()
    if rate.dir == 1:   # like post
        # return 409 if rating already exist
        if vote is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="rating already exist")
        new_rating = models.Rating(user_id=verified_user.id, post_id=rate.post_id)
        db.add(new_rating)
    elif rate.dir == 0:     # remove rating
        # return 404 if rating does not exist
        if vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="rating does not exist")
        rating.delete(synchronize_session=False)
    # commit changes into a database
    db.commit()
    return {"detail": "rating is saved"}

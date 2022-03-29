from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import utils, models, schemas
from ..database import get_db
from ..main import app


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # save hashed password
    user.password = utils.hash_password(user.password)
    # create single user
    new_user = models.User(**dict(user))  # unpack class as dictionary for easier input
    db.add(new_user)
    # commit changes into database
    db.commit()
    # return new user details
    db.refresh(new_user)
    return new_user


@app.get("/users/{id_}", response_model=schemas.UserResponse)
def get_user(id_: int, db: Session = Depends(get_db)):
    # get user by id
    user = db.query(models.User).filter_by(id=id_).first()
    # return 404 if user id was not found
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user was not found (id: {id_})")
    return user

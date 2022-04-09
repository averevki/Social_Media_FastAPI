"""Router with user queries"""
import re

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import database, utils, models, schemas

# declare router
router = APIRouter()

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    """Create new user and save him into the database"""
    if re.match(PASSWORD_REGEX, user.password) is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"password must contain at least 8 characters, one uppercase letter, "
                                   f"one lowercase letter, one number and one special character")
    # save hashed password
    user.password = utils.hash_password(user.password)
    # check if email already registered
    existence = db.query(models.User).filter(models.User.email == user.email).first()
    if existence is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email already registered (email: {user.email})")
    # create single user
    new_user = models.User(**dict(user))  # unpack class as dictionary for easier input
    db.add(new_user)
    # commit changes into database
    db.commit()
    # return new user details
    db.refresh(new_user)
    return new_user


@router.get("/{id_}", response_model=schemas.UserResponse)
def get_user(id_: int, db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    """Get user details by his id"""
    # get user by id
    user = db.query(models.User).filter_by(id=id_).first()
    # return 404 if user id was not found
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user was not found (id: {id_})")
    return user

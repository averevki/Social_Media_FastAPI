"""Router with user queries"""
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import database, utils, models, schemas

# declare router
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    """Add new user into the database

    Hashing user password

    :param user: scheme of user
    :param db: database dependency
    :return: user response scheme
    """
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


@router.get("/{id_}", response_model=schemas.UserResponse)
def get_user(id_: int, db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    """Get user details by his id

    :param id_: id of user to find
    :param db: database dependency
    :return: user response scheme
    """
    # get user by id
    user = db.query(models.User).filter_by(id=id_).first()
    # return 404 if user id was not found
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user was not found (id: {id_})")
    return user

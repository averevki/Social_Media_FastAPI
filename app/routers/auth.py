"""User login-in"""
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas, oauth2, utils

# declare router
router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Give user JWT for access to post operations

    OAuth2PasswordRequestForm getting data as form: {"username": "...", "password": "..."}

    :param user_credentials: user email and password
    :param db: database dependency
    :return: JWT for access
    """
    # find user by given email
    user = db.query(models.User).filter_by(email=user_credentials.username).first()
    # return 403 if user was not found
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    # check if passwords are the same
    if not utils.verify_password(password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    access_token: str = oauth2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}

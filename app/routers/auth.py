from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

# define router
router = APIRouter()


@router.post("/login")
def user_login(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # find user by given email
    user = db.query(models.User).filter_by(email=user_credentials.email).first()
    # return 404 if user was not found
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    # check if passwords are the same
    if utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    return {"token": "pepohappy"}

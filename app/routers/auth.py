from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models
from .. import utils, Oauth2



router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_details.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    check_password = utils.verify(user_details.password, user.password)

    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    access_token = Oauth2.create_access_token(data={"user_id": user.id, "user_email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

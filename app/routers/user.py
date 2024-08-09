from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. schemas import User, UserOut
from .. database import get_db
from .. import models
from .. utils import hash
from .. Oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: User, db: Session = Depends(get_db)):
    # Hash the passwd
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db), user_details: int = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

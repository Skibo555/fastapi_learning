from ..schemas import PostBase, PostCreate, Post, PostOut, UserOut
from ..database import get_db
from fastapi import HTTPException, status, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from typing import List
from ..Oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db), user_details: int = Depends(get_current_user)):
    # posts = db.query(models.Post).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(payload: PostCreate, db: Session = Depends(get_db),
                      user_details: int = Depends(get_current_user)):
    new_post = models.Post(owner_id=user_details.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostOut)
async def get_post(id: int, db: Session = Depends(get_db), user_details: int = Depends(get_current_user)):
    # result = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with the id {id} in our database.")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), user_details: int = Depends(get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with ID {id} in our database.")

    if user_details.id != result.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested action.")
    # result.delete(synchronize_session=False)
    db.delete(result)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
async def update(id: int, post_updated: PostBase, db: Session = Depends(get_db),
                 user_details: int = Depends(get_current_user)):
    result = (db.query(models.Post).filter(models.Post.id == id))
    post = result.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Our record does not match the ID {id} you provided")
    if user_details.id != result.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested action.")
    result.update(post_updated.dict(), synchronize_session=False)
    db.commit()
    return post

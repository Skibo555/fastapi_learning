from fastapi import Depends, APIRouter, HTTPException, status
from .. schemas import Vote
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models
from .. import Oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, db: Session = Depends(get_db), user_details: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {vote.post_id}.")
    """
           This queries the Vote Model and filters base off post ID passed in the payload which is vote (pydantic model)
           in this case to the post_id in the Vote Model and to get the post where current_user.id is only == to
           Vote.user_id in the Vote Database Model.

           this helps to get only the vote by the current user.
    """
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                                models.Vote.user_id == user_details.id)
    found_vote = vote_query.first()

    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {user_details.id} has already voted on this post")
        new_vote = models.Vote(post_id=vote.post_id, user_id=user_details.id)
        db.add(new_vote)
        db.commit()
        return {
            "message": "Successfully voted!",
            "status_code": status.HTTP_201_CREATED
        }
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You haven't voted on this post!")
        db.delete(found_vote)
        db.commit()
        return {
            "message": "You have un-voted this post.",
            "status": status.HTTP_204_NO_CONTENT
        }

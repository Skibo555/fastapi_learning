from pydantic import BaseModel, EmailStr
from datetime import datetime
import email_validator
from typing import Optional
from pydantic import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes=True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes=True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    owner_details: UserOut

    class Config:
        from_attributes=True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes=True


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes=True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes=True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes=True


class TokenData(BaseModel):
    id: Optional[int] = None
    user_email: EmailStr

    class Config:
        from_attributes=True


class Vote(BaseModel):
    post_id: int
    # This ensures that the vote_dir is either 0 or 1
    vote_dir: conint(le=1, gt=-1)

    class Config:
        from_attributes=True


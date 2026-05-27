from sqlmodel import Session, select
from typing import Annotated
from fastapi import HTTPException, Depends, Response
import bcrypt
import jwt
from app.db import get_session
from fastapi import  Depends, status, HTTPException, Response, Cookie
from app.model.user.user import User
from app.model.book.book import Book

SECRET = "supersecret"
ALGORITHM = "HS256"


SessionDep = Annotated[Session, Depends(get_session)]


async def get_all_books(session: SessionDep, auth: Annotated[ str | None,  Cookie()]= None ):
    if auth == None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detailes = "Please log in")

    id = jwt.decode(auth, SECRET, algorithm = ALGORITHM)

    found_user = session.get(User, id)

    if not found_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ="Please log in")

    return {"message": "Blogs"}
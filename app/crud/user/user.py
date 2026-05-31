from sqlmodel import Session, select
from typing import Annotated
from fastapi import HTTPException, Depends, Response, status
import bcrypt
import jwt
from app.schema.user.user import LoginRequest, RegisterRequest
from app.db import get_session
from app.model.book.book import Book

from app.model.user.user import User

SECRET = "supersecret"
ALGORITHM = "HS256"


SessionDep = Annotated[Session, Depends(get_session)]

async def Register(user: RegisterRequest, session: SessionDep):

    found_user = session.exec(select(User).where(User.email == user.email)).first()

    if found_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is useb by another account")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "success"}



async def Login(user: LoginRequest, session: SessionDep, response: Response):

    found_user = session.exec(select(User).where(User.email == user.email)).first()
    if not found_user or not bcrypt.checkpw(user.password.encode(), found_user.password.encode()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Incorrect username or password")


    token = jwt.encode({"user_id":  found_user.id }, SECRET, algorithm = ALGORITHM)
    response.set_cookie(key="authsession", value=token, secure=True, httponly=True)
    return {"message": "success"}

async def Logout(response: Response):
    response.delete_cookie(key="authsession", secure=True, httponly=True)
    return {"message": "success"}



async def Get_books(session: SessionDep, auth: Annotated[ str | None,  Cookie()]= None ):
    if auth == None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Please log in")

    payload = jwt.decode(auth, SECRET, algorithm = ALGORITHM)

    found_user = session.get(User, payload["user_id"])

    if not found_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ="Please log in")


    return {"books": found_user.bookes}
from sqlmodel import Session, select
from typing import Annotated
from fastapi import HTTPException, Depends, Response
import bcrypt
import jwt

from app.model.user.user import User

SECRET = "supersecret"
ALGORITHM = "HS256"


SessionDep = Annotated[Session, Depends(get_session)]

async def register(user: RegisterRequest, session: SessionDep, response:Response):

    found_user = session.exec(select(User).where(User.email == user.email)).first()

    if found_user:
        raise HTTPException(status_code=409, detail="Email is useb by another account")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "success"}



async def login(user: LoginRequest, session: SessionDep, response: Response):

    found_user = session.exec(select(User).where(User.email == user.email)).first()
    if not found_user or not bcrypt.checkpw(user.password.encode(), found_user["password"].encode()):
        raise HTTPException(status_code=404,detail ="Incorrect username or password")


    token = jwt.encode({"user_id":  found_user.id }, SECRET, algorithm = ALGORITHM)
    response.set_cookie(key="authsession", value=token, secure=True, httponly=True)
    return {"message": "success"}

def logout(response: Response):
    response.delete_cookie(key="authsession", secure=True, httponly=True)
    return {"message": "success"}
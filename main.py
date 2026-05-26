from fastapi import FastAPI, Response, Depends, HTTPException
import jwt
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from pydantic import BaseModel
import bcrypt

from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import status

SECRET = "supersecret"
ALGORITHM = "HS256"



class User(SQLModel, table=True):
    id: int | None=Field(default = None, primary_key = True)
    name:  str = Field(index =True)
    email: str= Field(index = True)
    password: str =Field(index =True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]



app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


security = HTTPBasic()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str





@app.get("/",status_code=status.HTTP_200_OK)
def create_root():
    return {"message": "Main route"}




@app.post("/register", status_code=status.HTTP_201_CREATED)
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


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginRequest, session: SessionDep, response: Response):

    found_user = session.exec(select(User).where(User.email == user.email)).first()
    if not found_user or not bcrypt.checkpw(user.password.encode(), found_user["password"].encode()):
        raise HTTPException(status_code=404,detail ="Incorrect username or password")


    token = jwt.encode({"user_id":  found_user.id }, SECRET, algorithm = ALGORITHM)
    response.set_cookie(key="authsession", value=token, secure=True, httponly=True)
    return {"message": "success"}





@app.get("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.delete_cookie(key="authsession", secure=True, httponly=True)
    return {"message": "success"}
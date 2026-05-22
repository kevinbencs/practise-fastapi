from fastapi import FastAPI, Response, Depends, HTTPException
import jwt
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentails
import secrets
from pydantic import BaseModel
import bcrypt

from sqlmodel import Field, Session, SQLModel, crete_engine,  select

SECERT = "supersecret"
ALGORITHM = "HS256"



class User(SQLModel, talble=True):
    id: int | None=Field(default = None, primary_key = True)
    name:  str = Field(index =True)
    email: str= Field(index = True)
    password: str =Field(index =True)


sqlitte_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlitte_file_name}"

def creatq_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]



app = FastAPI()

app.on_event("startup")
def on_startup():
    creatq_db_and_tables()


security = HTTPBasic()


class LoginRequest(Base):
    email: str
    password: str


class RegisterRequest(Base):
    email: str
    password: str
    name: str



#def get_current_username(
#        credentials: Annotated[HTTPBasicCredentails, Depends(security)],
#):
#    current_username_bytes = credentials.username.encode("utf8")
#    correct_username_bytes = b"stanleyjobson"
#    is_correct_username = secrets.compare_digest(
#        current_username_bytes, correct_username_bytes
#    )
#
#    current_password_bytes = credentials.password.encode("utf8")
#    correct_password_bytes = b"swordfish"
#    is_correct_password = secrets.compare_digest(
#        current_password_bytes,  correct_password_bytes
#    )
#    if not (is_correct_password and is_correct_username):
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"www-Authenticate": "Basic"}
#        )
#    return credentials.username



@app.get("/")
def reat_root(status_code: 200):
    return {"message": "Main route"}


#@app.get("/user/me")
#def get_user(credentails: Annotated[HTTPBasicCredentails, Depends(security)]):
#    return {"username": credentails.username, "pssword": credentails.password}


#@app.get("/user/me")
#def get_user(username: Annotated[str, Depends(get_current_username)],status_code: 200):
#    return {"username": username}



#@app.post("/register")
#def register(email: str, password: str, status_code: 201):
#    return {"message": "success"}
#
#@app.post("/login")
#def login(username: Annotated[str, Depends(get_current_username)], response: Response, status_code: 200):
#    token = jwt.encode({"user_name":  username , SECRET, algorithm = ALGORITHM})
#    response.set_cookie(key="authsession", value=token, secure=True, httponly=True)
#    return {"message": "success"}



@app.post("/register")
async def register(user: RegisterRequest, session: SessionDep, response:Response, status_code: 201):

    found_user = session.get(User,user.email)

    if found_user:
        raise HTTPException(status_code=409, detail="Email is useb by another account")

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "success"}


@app.post("/login")
async def login(user: LoginRequest, session: SessionDep, response: Response, status_code: 200):

    found_user = session.get(User, user.email)
    if not found_user or not bcrypt.checkpw(user.password.encode(), found_user["password"].encode()):
        raise HTTPException(status_code=404,detail ="Incorrect username or password")


    token = jwt.encode({"user_id":  found_user["user_id"] , SECRET, algorithm = ALGORITHM})
    response.set_cookie(key="authsession", value=token, secure=True, httponly=True)
    return {"message": "success"}



#
#
#@app.get("/logout")
#def logout(response: Response, status_code: 200):
#    response.delete_cookie(key="authsession", secure=True, httponly=True)
#    return {"message": "success"}
from fastapi import FastAPI, Response
import jwt
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError

app = FastAPI()

@app.get("/")
def reat_root(status_code: 200):
    return {"message": "Main route"}


@app.post("/register")
def register(email: str, password: str, status_code: 201):
    return {"message": "success"}

@app.post("/login")
def login(email: str, password: str, response: Response, status_code: 200):

    response.set_cookie(key="authsession", value="token", secure=True, httponly=True)
    return {"message": "success"}


@app.get("/logout")
def logout(response: Response, status_code: 200):
    response.delete_cookie(key="authsession", secure=True, httponly=True)
    return {"message": "success"}
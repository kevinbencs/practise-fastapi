from sqlmodel import Session, select
from typing import Annotated
from fastapi import HTTPException, Depends, Response
import bcrypt
import jwt
from app.db import get_session
from fastapi import  Depends, status, HTTPException, Response, Cookie
from app.model.user.user import User
from app.model.book.book import Book
from app.db import SessionDep

SECRET = "supersecret"
ALGORITHM = "HS256"




async def get_all_books():
    

    return {"message": "Blogs"}
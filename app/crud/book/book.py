from sqlmodel import Session, select
from typing import Annotated
from fastapi import HTTPException, Depends, Response
import bcrypt
import jwt
from fastapi import  Depends, status, HTTPException, Response, Cookie
from app.model.user.user import User
from app.model.book.book import Book
from app.db import SessionDep, get_session

SECRET = "supersecret"
ALGORITHM = "HS256"




async def get_all_books(session: SessionDep,  ):

    books = session.exec(select(Book))

    return {"Books": books}


async def Get_book_id(session: SessionDep, item_id: int):
    book = session.get(Book, item_id)

    return {"book": book}


async def Add_book(session: SessionDep, name: str, detail: str):
    db_book = Book(name, detail)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return {"message": "success"}
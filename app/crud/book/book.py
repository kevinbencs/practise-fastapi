from sqlmodel import select
from typing import Annotated
from fastapi import  Depends, status, HTTPException
from app.model.book.book import Book
from app.db import SessionDep

SECRET = "supersecret"
ALGORITHM = "HS256"




async def get_all_books(session: SessionDep,  ):

    books = session.exec(select(Book)).all()

    return {"Books": books}


async def Get_book_id(session: SessionDep, item_id: int):
    book = session.get(Book, item_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Book not found")
    return {"book": book}


async def Add_book(session: SessionDep, name: str, detail: str):
    db_book = Book(name=name, detail=detail)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return {"message": "success"}
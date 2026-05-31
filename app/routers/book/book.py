from fastapi import APIRouter, Depends, status,  Response, Cookie
from app.db import SessionDep
import jwt
from app.crud.book.book import get_all_books, Get_book_id, Add_book


SECRET = "supersecret"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/book",
    tags=['Book']
)


@router.get("/",status_code=status.HTTP_200_OK)
def get_books(session: SessionDep ):
    return get_all_books(session)

@router.get("/id/{item_id}", status_code=status.HTTP_200_OK)
def get_book_id(session: SessionDep, item_id: int):
    return Get_book_id(session, item_id)


@router.post("/book/add", status_code=status.HTTP_201_CREATED)
def add_book(session: SessionDep, name: str, detail: str):
    return Add_book(session, name, detail)
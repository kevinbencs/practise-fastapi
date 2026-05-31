from fastapi import APIRouter, Depends, status,  Response, Cookie
from app.db import SessionDep
import jwt
from app.crud.book.book import get_all_books, Get_book_id, Add_book
from app.schema.book.book import AddBook

router = APIRouter(
    prefix="/book",
    tags=['Book']
)


@router.get("/",status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep ):
    return await et_all_books(session)

@router.get("/id/{item_id}", status_code=status.HTTP_200_OK)
async def get_book_id(session: SessionDep, item_id: int):
    return await Get_book_id(session, item_id)


@router.post("/book/add", status_code=status.HTTP_201_CREATED)
async def add_book(session: SessionDep, book: AddBook):
    return await Add_book(session, name=book.name, detail=book.detail)
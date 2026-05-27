from fastapi import APIRouter, Depends, status,  Response, Cookie
from app.db import SessionDep
import jwt
from app.crud.book.book import get_all_books


SECRET = "supersecret"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)


@router.get("/",status_code=status.HTTP_200_OK)
def get_books(session: SessionDep, auth: Annotated[ str | None,  Cookie()]= None ):
    return get_all_books(session, auth)
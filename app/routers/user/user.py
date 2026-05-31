from fastapi import Response,  status, APIRouter, Cookie
from app.db import create_db_and_tables
from app.crud.user.user import Login, Register, Logout, SessionDep, Get_books
from app.schema.user.user import LoginRequest, RegisterRequest
from typing import Annotated

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: RegisterRequest, session: SessionDep):
    return await Register(user, session)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginRequest, session: SessionDep, response: Response):
    return await Login(user, session, response)


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    return await Logout(response)


@router.get("/book", status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep, auth: Annotated[ str | None,  Cookie()]= None ):
    return await Get_books(session, auth)
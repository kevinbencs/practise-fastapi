from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
import jwt

SECRET = "supersecret"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)

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


@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_books(session: SessionDep, auth: Annotated[ str | None,  Cookie()]= None ):
    if auth == None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detailes = "Please log in")

    id = jwt.decode(auth, SECRET, algorithm = ALGORITHM)

    found_user = session.get(User, id)

    if not found_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ="Please log in")

    return {"message": "Blogs"}
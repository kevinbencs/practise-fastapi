from fastapi import FastAPI
from fastapi.security import HTTPBasic
from app.db import create_db_and_tables
from app.routers.user.user import router as user_router
from app.routers.book.book import router as book_router
from fastapi import status
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/",status_code=status.HTTP_200_OK)
def create_root():
    return {"message": "Main route"}


app.include_router(book_router)
app.include_router(user_router)

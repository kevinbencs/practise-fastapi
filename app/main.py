from fastapi import FastAPI
from fastapi.security import HTTPBasic
from app.db import create_db_and_tables
from app.routers.user.user import router as user_router
from app.routers.book.book import router as book_router
from fastapi import status
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .mongo_models import LogEntry


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    client = AsyncIOMotorClient("mongodb://...")
    await init_beanie(database=client.my_fastapi_mongo_db, document_models=[LogEntry])
    yield
    client.close(),



app = FastAPI(lifespan=lifespan)


@app.get("/",status_code=status.HTTP_200_OK)
async def create_root():
    log = LogEntry(event="Someone visited this route", level="INFo")
    await log.insert()
    return {"message": "Main route"}


app.include_router(book_router)
app.include_router(user_router)



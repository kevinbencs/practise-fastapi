from sqlmodel import Field, Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
import os

##sqlite_file_name = "database.db"

##sqlite_url = f"sqlite:///{sqlite_file_name}"

DB_URL = os.getenv("DTABASE_URL", "postgresql:user:....")
##connect_args = {"check_same_thread":False}
##engine = create_engine(sqlite_url, connect_args=connect_args)
engine = create_engine(DB_URL)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

async def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

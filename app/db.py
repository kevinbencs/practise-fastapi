from sqlmodel import Field, Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
from app.config import get_settings


##sqlite_file_name = "database.db"

##sqlite_url = f"sqlite:///{sqlite_file_name}"


##connect_args = {"check_same_thread":False}
##engine = create_engine(sqlite_url, connect_args=connect_args)
#engine = create_engine(DB_URL)




settings = get_settings()
engine = create_engine(settings.database_url)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

async def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

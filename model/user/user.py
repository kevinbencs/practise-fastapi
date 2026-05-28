from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from typing import List
from app.model.book.book import Book



class User(SQLModel, table=True):
    id: int | None=Field(default = None, primary_key = True)
    name:  str = Field(index =True)
    email: str= Field(index = True)
    password: str =Field(index =True)
    bookes: List[Book] = Relationship(back_populates="user")
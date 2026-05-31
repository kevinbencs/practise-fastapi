from sqlmodel import Field, SQLModel, Relationship
from typing import List
from app.model.book.book import Book



class User(SQLModel, table=True):
    id: int | None=Field(default = None, primary_key = True)
    name:  str = Field(index =True)
    email: str= Field(index = True)
    password: str =Field(index =True)
    books: List[Book] = Relationship(back_populates="user")
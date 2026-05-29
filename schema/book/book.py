from pydantic import BaseModel


class AddBook(BaseModel):
    name: str
    detail: str
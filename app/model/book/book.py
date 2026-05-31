from sqlmodel import Field,  SQLModel, Relationship

class Book(SQLModel, table=True):
    id: int | None=Field(default = None, primary_key = True)
    name:  str = Field(index =True)
    detail: str = Field()
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="books")

from fastapi import Response,  status, APIRouter
from app.db import create_db_and_tables
from app.crud.user.user import Login, Register, Logout, SessionDep
from app.schema.user.user import LoginRequest, RegisterRequest

router = APIRouter(
    prefix="/user",
    tags=['User']
)

router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterRequest, session: SessionDep, response:Response):
    return Register(user, session, response)

router.post("/login", status_code=status.HTTP_200_OK)
def login(user: LoginRequest, session: SessionDep, response: Response):
    return Login(user, session, response)


router.get("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    return Logout(response)
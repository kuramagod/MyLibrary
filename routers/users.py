from typing import Annotated

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from models import UserPublic, UserCreate, Token, User
from dependencies import SessionDep, pwd_context, User, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user


router = APIRouter(prefix="/users", tags=["users"])


#Пользователи
@router.post("/register/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep) -> User:
    hashed_pwd = pwd_context.hash(user.password)
    user_data = user.model_dump() # Превращаем тело запроса, объект Pydantic модели UserCreate, в обычный словарь.
    user_data["hashed_password"] = hashed_pwd
    del user_data["password"]

    db_user = User(**user_data)
    session.add(db_user)
    
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data")
    
    session.refresh(db_user)
    return db_user


@router.post("/login/", response_model=Token)
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserPublic)
def read_user_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
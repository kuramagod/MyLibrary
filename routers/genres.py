from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from models import Genre, GenrePublic, GenreCreate, User
from dependencies import SessionDep, is_admin


router = APIRouter(prefix="/genres")


# Жанры
@router.get("/", response_model=list[GenrePublic])
def read_genres(session: SessionDep) -> Genre:
    genres = session.exec(select(Genre)).all()
    return genres

@router.post("/", response_model=Genre)
def create_genre(
    genre: GenreCreate,
    current_user: Annotated[User, Depends(is_admin)],
    session: SessionDep
    ) -> Genre:
    db_genre = Genre.model_validate(genre)
    session.add(db_genre)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre already exists")
    session.refresh(db_genre)
    return db_genre
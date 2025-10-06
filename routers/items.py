from typing import Annotated
from sqlalchemy import func
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from models import ItemPublic, Item, ItemCreate, ItemUpdate, Genre, User, Review
from dependencies import SessionDep, is_admin


router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemPublic])
def read_items(
    session: SessionDep,
    genre: Annotated[str | None, Query(min_length=3)] = None,
    release_year: Annotated[int | None, Query(ge=0, le=datetime.today().year)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(le=100)] = 100,
    title:  Annotated[str | None, Query(max_length=255)] = None) -> Item:
    query = select(Item)
    
    if genre:
        db_genre = session.exec(select(Genre).where(Genre.name == genre)).first()
        if not db_genre:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Genre not found")
        query = query.where(Item.genre_id == db_genre.id)
    
    if release_year:
        query = query.where(Item.release_year == release_year)
    
    if title:
        query = query.where(Item.title.ilike(f"%{title}%"))
    
    query = query.order_by(Item.id)
    return session.exec(query.offset((page - 1) * size).limit(size)).all()


@router.get("/{item_id}", response_model=ItemPublic)
def read_item(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    avg_rating = session.exec(
        select(func.avg(Review.rating))
        .where(Review.item_id == item_id)
    ).one()
    return {**item.__dict__, "avg_rating": avg_rating}


@router.post("/", response_model=Item)
def create_item(
    item: ItemCreate, 
    current_user: Annotated[User, Depends(is_admin)],
    session: SessionDep,
    ) -> Item:
    db_item = Item.model_validate(item)
    session.add(db_item)
    try: 
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data (duplicate or foreign key error)")
    session.refresh(db_item)
    return db_item


@router.patch("/{item_id}", response_model=ItemPublic)
def update_item(
    item_id: int, 
    item: ItemUpdate,
    current_user: Annotated[User, Depends(is_admin)], 
    session: SessionDep
    ) -> Item:
    item_db = session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    item_data = item.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(item_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    current_user: Annotated[User, Depends(is_admin)],
    session: SessionDep
    ) -> dict:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(item)
    session.commit()
    return {"OK": True}
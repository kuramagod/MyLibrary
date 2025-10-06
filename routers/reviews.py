from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from models import User, Review, ReviewCreate, ReviewPublic, ReviewUpdate
from dependencies import get_current_user, SessionDep


router = APIRouter(prefix="/reviews")

# Рецензии
@router.post("/", response_model=ReviewPublic)
def create_review(
    current_user: Annotated[User, Depends(get_current_user)],
    review: ReviewCreate, 
    session: SessionDep
    ) -> Review:
    review_data = review.model_dump()
    review_data["user_id"] = current_user.id
    db_review = Review.model_validate(review_data)
    session.add(db_review)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data")
    session.refresh(db_review)
    return db_review


@router.get("/reviews/item/{item_id}", response_model=list[Review])
def item_reviews(item_id: int, session: SessionDep) -> Review:
    item_reviews = session.exec(select(Review).where(Review.item_id == item_id)).all()
    return item_reviews 


@router.get("/reviews/user/{user_id}", response_model=list[Review])
def user_reviews(user_id: int, session: SessionDep) -> Review:
    user_reviews = session.exec(select(Review).where(Review.user_id == user_id)).all()
    return user_reviews


@router.patch("/review/{review_id}/", response_model=ReviewPublic)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> Review:
    review_db = session.get(Review, review_id)
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if review_db.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    review_data = review.model_dump(exclude_unset=True)
    review_db.sqlmodel_update(review_data)
    session.add(review_db)
    session.commit()
    session.refresh(review_db)
    return review_db


@router.delete("/review/{review_id}/")
def delete_item(review_id: int, 
                session: SessionDep,
                current_user: Annotated[User, Depends(get_current_user)]
                ) -> dict:
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    session.delete(review)
    session.commit()
    return {"OK": True}
from sqlmodel import SQLModel, Field, Column, String, Relationship, DateTime, func, Integer
from pydantic import EmailStr
from datetime import datetime, timezone


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class UserRole(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), unique=True))
    users: list["User"] = Relationship(back_populates="role")


class UserBase(SQLModel):
    username: str = Field(sa_column=Column(String(25), unique=True, nullable=False))
    email: str = Field(sa_column=Column(String(100), unique=True, nullable=False))


class User(UserBase,  table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(sa_column=Column(String(128), nullable=False))
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False))
    role_id: int = Field(default=1, foreign_key="userrole.id")
    role: UserRole | None = Relationship(back_populates="users")


class UserPublic(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    username: str = Field(max_length=25, regex=r"^\S+$", description="Username cannot contain spaces")
    email: str = Field(max_length=100)
    password: str = Field(max_length=128)


class UserUpdate(SQLModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    model_config = {
        "extra": "forbid"
    }


class GenreBase(SQLModel):
    name: str = Field(sa_column=Column(String(50), unique=True, nullable=False))


class Genre(GenreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class GenreCreate(GenreBase):
    pass


class GenrePublic(GenreBase):
    id: int


class ItemBase(SQLModel):
    title: str
    description: str
    release_year: int
    genre_id: int


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    description: str = Field()
    release_year: int = Field(ge=0, le=datetime.today().year)
    genre_id: int = Field(foreign_key="genre.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ItemCreate(ItemBase):
    release_year: int = Field(ge=0, le=datetime.today().year)


class ItemPublic(ItemBase):
    id: int
    created_at: datetime
    avg_rating: float | None = None


class ItemUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    release_year: int | None = None
    genre_id: int | None = None

    model_config = {
        "extra": "forbid"
    }


class ReviewBase(SQLModel):
    item_id: int
    rating: int
    comment: str


class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    item_id: int = Field(foreign_key="item.id")
    rating: int = Field(ge=1, le=10)
    comment: str = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReviewCreate(ReviewBase):
    pass


class ReviewPublic(ReviewBase):
    user_id: int


class ReviewUpdate(SQLModel):
    rating: int | None = None
    comment: str | None = None

    model_config = {
        "extra": "forbid"
    }
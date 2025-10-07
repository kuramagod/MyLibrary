from sqlmodel import SQLModel, Field, Column, String, Relationship, DateTime, func
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
    role: UserRole


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
    items: list["Item"] = Relationship(back_populates="genre")


class GenreCreate(GenreBase):
    name: str = Field(max_length=50)


class GenrePublic(GenreBase):
    id: int


class ItemBase(SQLModel):
    title: str = Field(sa_column=Column(String(50), nullable=False))
    description: str = Field(sa_column=String(250))
    release_year: int = Field(ge=0, le=datetime.today().year)


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    genre_id: int = Field(foreign_key="genre.id")
    genre: Genre | None = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    title: str = Field(max_length=50)
    description: str = Field(max_length=250)
    release_year: int = Field(ge=0, le=datetime.today().year)
    genre_id: int


class ItemPublic(ItemBase):
    id: int
    created_at: datetime
    genre: Genre
    avg_rating: float | None = None


class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=250)
    release_year: int | None = Field(default=None, ge=0, le=datetime.today().year)
    genre_id: int | None = None

    model_config = {
        "extra": "forbid"
    }


class ReviewBase(SQLModel):
    item_id: int = Field(foreign_key="item.id")
    rating: int = Field(ge=1, le=10)
    comment: str = Field(String(250))


class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReviewCreate(ReviewBase):
    comment: str = Field(max_length=250)


class ReviewPublic(ReviewBase):
    user_id: int


class ReviewUpdate(ReviewBase):
    rating: int | None = Field(default=None, ge=1, le=10)
    comment: str | None = Field(default=None, max_length=250)

    model_config = {
        "extra": "forbid"
    }
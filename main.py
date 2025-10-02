from fastapi import FastAPI
from app.routers import items, users, genres, reviews
from app.database import create_db_and_tables


app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(genres.router)
app.include_router(reviews.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
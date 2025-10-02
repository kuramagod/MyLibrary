from sqlmodel import SQLModel, create_engine, Session


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connection_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connection_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# For SQLite Database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sqlite.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread" : False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
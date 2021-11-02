import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from project.config import settings


engine = create_engine(os.environ['DATABASE_URL'])
engine = create_engine(os.environ['DATABASE_URL'], connect_args=settings.DATABASE_CONNECT_DICT
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
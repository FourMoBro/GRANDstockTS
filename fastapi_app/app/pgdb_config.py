import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

PG_URL2 = os.environ.get("PG_URL")

engine = create_engine(
    PG_URL2
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
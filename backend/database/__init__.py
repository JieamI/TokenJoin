from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os



SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}".format(os.getenv("TOKEN_JOIN_USER"), os.getenv("TOKEN_JOIN_PASSWORD"), os.getenv("TOKEN_JOIN_HOST"), os.getenv("TOKEN_JOIN_DB"))

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
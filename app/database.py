from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://user:password@localhost/comparathor"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Get a database session.

    Yields
    ------
    Session
        The database session to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

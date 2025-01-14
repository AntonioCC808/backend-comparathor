from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = None
SessionLocal = None


Base = declarative_base()


def init_db(db_url: str):
    """
    Initialize the database with the given connection URL.

    This function creates a SQLAlchemy engine, sets up a session factory bound
    to this engine, and generates all defined tables in the database schema
    if they do not already exist.

    Parameters
    ----------
    db_url : str
        The database connection URL. It should follow SQLAlchemy's URL format,
        e.g., 'sqlite:///test.db' or 'mysql+pymysql://user:password@localhost/dbname'.
    """
    global engine, SessionLocal
    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to provide a SQLAlchemy session.

    Yields
    ------
    Session
        A database session for use in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
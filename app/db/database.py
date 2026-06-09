# db/database.py
# Sets up the connection to PostgreSQL using SQLAlchemy.
# Think of SQLAlchemy as a translator between Python and SQL.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# The "engine" is the actual connection to the database
engine = create_engine(DATABASE_URL)

# A "session" is like a conversation with the database — you open one,
# do your reads/writes, then close it.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our table models will inherit from
Base = declarative_base()


def get_db():
    """
    FastAPI dependency — gives a route a database session, then closes it
    automatically when the request is done (the 'finally' block always runs).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Called once at startup.
    Creates all tables defined in models.py if they don't exist yet.
    """
    Base.metadata.create_all(bind=engine)
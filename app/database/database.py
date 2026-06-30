from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import logging

load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

def get_db():
    """
    FastAPI database dependency.
    Creates a new database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def test_connection():
    """
    Test the database connection by excuting a simple query."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("✅ MySQL connection successful")
            print("✅ MySQL connection successful")
            return True

    except Exception as e:
        logger.error(f"❌ MySQL connection failed: {e}")
        print(f"❌ MySQL connection failed: {e}")
        return False

from app.database import models

def init_db():
    """Creates all database tables defined in models.py if they don't exist."""
    Base.metadata.create_all(bind=engine)
    

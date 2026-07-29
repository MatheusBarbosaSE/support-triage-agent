from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the SQLite database URL (it will create a file named 'tickets.db' in the root)
SQLALCHEMY_DATABASE_URL = "sqlite:///./tickets.db"

# 2. Create the SQLAlchemy engine
# Tip: SQLite requires 'check_same_thread': False for FastAPI concurrency
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class for database sessions
# autocommit=False prevents accidental saves, autoflush=False prevents premature queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to yield a database session and close it automatically.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
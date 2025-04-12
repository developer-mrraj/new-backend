from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://fastapi_user:yourpassword@localhost/crm_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create_engine(SQLALCHEMY_DATABASE_URL) → Connects FastAPI to the SQLite database.
# SessionLocal → Creates database sessions to interact with tables.
# Base = declarative_base() → Serves as the base class for defining database models.


# Create base class for models
Base = declarative_base()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()     
        
        # connect_args={"check_same_thread": False}
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . config import settings

SQLALCHEMEY_DATABASE_URI = (f"{settings.DATABASE_TYPE}://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
                            f"@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}")

engine = create_engine(SQLALCHEMEY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

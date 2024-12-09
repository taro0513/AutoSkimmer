from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from model import Base
from config import config

engine = create_engine(
    config.TASK_DB, connect_args={"check_same_thread": False}
)

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        raise
    finally:
        db.close()

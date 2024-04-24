from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_FILE_PATH = './vin_cache.db'

Engine = create_engine(
  f'sqlite:///{SQLITE_FILE_PATH}',
  connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()

def get_db_session():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

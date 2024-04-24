import os
from fastapi import FastAPI
from backend.app.db.connection import Base, Engine, SQLITE_FILE_PATH
from backend.app.features import lookup

# Remove the sqlite cache at startup
if os.path.exists(SQLITE_FILE_PATH):
  os.remove(SQLITE_FILE_PATH)

# Create all tables
Base.metadata.create_all(bind=Engine)

app = FastAPI()
app.include_router(lookup.router)

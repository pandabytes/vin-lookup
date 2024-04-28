import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.connection import Base, Engine, SQLITE_FILE_PATH
from .features import lookup
from .features import remove
from .features import export
from .features import list_vins

# Remove the sqlite cache at startup
if os.path.exists(SQLITE_FILE_PATH):
  os.remove(SQLITE_FILE_PATH)

# Create all tables
Base.metadata.create_all(bind=Engine)

app = FastAPI()

# TODO: update this to allow certain origins only
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lookup.router)
app.include_router(remove.router)
app.include_router(export.router)
app.include_router(list_vins.router)

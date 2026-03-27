from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.bootstrap import bootstrap_remote_database, ensure_site_settings_schema, ensure_teachers_schema, sync_postgres_sequences
from app.database import Base, STATIC_DIR, SessionLocal, engine
from app.routers import admin, public
from app.seed import init_db

_database_initialized = False


def initialize_database() -> None:
    global _database_initialized
    if _database_initialized:
        return

    Base.metadata.create_all(bind=engine)
    ensure_site_settings_schema()
    ensure_teachers_schema()
    bootstrap_remote_database()
    sync_postgres_sequences()

    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    _database_initialized = True


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Denov 2 School", lifespan=lifespan)

initialize_database()

if STATIC_DIR.exists() and not os.getenv("VERCEL"):
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(public.router)
app.include_router(admin.router, prefix="/admin")

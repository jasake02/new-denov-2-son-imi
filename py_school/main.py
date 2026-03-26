from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.bootstrap import bootstrap_remote_database
from app.database import Base, STATIC_DIR, SessionLocal, engine
from app.routers import admin, public
from app.seed import init_db


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    bootstrap_remote_database()

    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Denov 2 School", lifespan=lifespan)

if STATIC_DIR.exists() and not os.getenv("VERCEL"):
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(public.router)
app.include_router(admin.router, prefix="/admin")

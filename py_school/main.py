from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base, SessionLocal
from app.seed import init_db
from app.routers import public, admin

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize database with seed data
db = SessionLocal()
try:
    init_db(db)
finally:
    db.close()

app = FastAPI(title="Denov 2 School")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(public.router)
app.include_router(admin.router, prefix="/admin")


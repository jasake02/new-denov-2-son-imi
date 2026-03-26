import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
APP_DIR = BASE_DIR / "app"
PUBLIC_DIR = PROJECT_ROOT / "public"
LEGACY_STATIC_DIR = APP_DIR / "static"
STATIC_DIR = PUBLIC_DIR / "static" if (PUBLIC_DIR / "static").exists() else LEGACY_STATIC_DIR
TEMPLATES_DIR = APP_DIR / "templates"
DATABASE_PATH = BASE_DIR / "school.db"


def _discover_database_env() -> str | None:
    def is_database_url(value: str | None) -> bool:
        if not value:
            return False
        normalized = value.strip().lower()
        return normalized.startswith(("postgres://", "postgresql://", "prisma+postgres://", "sqlite:///"))

    explicit_keys = (
        "DATABASE_URL",
        "POSTGRES_URL",
        "POSTGRES_URL_NON_POOLING",
        "POSTGRES_PRISMA_URL",
    )
    for key in explicit_keys:
        value = os.getenv(key)
        if is_database_url(value):
            return value

    suffixes = (
        "_DATABASE_URL",
        "_URL_NON_POOLING",
        "_POSTGRES_URL",
        "_URL",
        "_PRISMA_URL",
    )
    preferred_tokens = ("DATABASE", "POSTGRES", "NEON", "STORAGE")

    for suffix in suffixes:
        for key, value in os.environ.items():
            if suffix != "_PRISMA_URL" and "PRISMA" in key:
                continue
            if (
                is_database_url(value)
                and key.endswith(suffix)
                and any(token in key for token in preferred_tokens)
            ):
                return value

    return None


def _normalize_database_url(value: str | None) -> str:
    if not value:
        return f"sqlite:///{DATABASE_PATH.as_posix()}"

    normalized = value.strip()
    if normalized.startswith("prisma+postgres://"):
        normalized = normalized.replace("prisma+postgres://", "postgresql+psycopg://", 1)
    elif normalized.startswith("postgres://"):
        normalized = normalized.replace("postgres://", "postgresql+psycopg://", 1)
    elif normalized.startswith("postgresql://"):
        normalized = normalized.replace("postgresql://", "postgresql+psycopg://", 1)
    return normalized

SQLALCHEMY_DATABASE_URL = _normalize_database_url(_discover_database_env())
IS_SQLITE = SQLALCHEMY_DATABASE_URL.startswith("sqlite")

engine_kwargs = {"pool_pre_ping": True}
if IS_SQLITE:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["poolclass"] = NullPool

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

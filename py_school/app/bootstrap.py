import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database import DATABASE_PATH, IS_SQLITE, SessionLocal
from app.models.models import AdminUser, ContentItem, ContactMessage, Department, News, SiteSetting, Teacher

BOOTSTRAP_MODELS = (
    AdminUser,
    SiteSetting,
    ContentItem,
    Department,
    News,
    Teacher,
    ContactMessage,
)


def sync_postgres_sequences() -> None:
    if IS_SQLITE:
        return

    db = SessionLocal()
    try:
        for model in BOOTSTRAP_MODELS:
            table = model.__table__.name
            primary_keys = list(model.__table__.primary_key.columns)
            if len(primary_keys) != 1:
                continue

            pk = primary_keys[0].name
            max_id = db.execute(text(f"SELECT COALESCE(MAX({pk}), 0) FROM {table}")).scalar_one()

            if max_id > 0:
                db.execute(
                    text("SELECT setval(pg_get_serial_sequence(:table_name, :column_name), :value, true)"),
                    {"table_name": table, "column_name": pk, "value": max_id},
                )
            else:
                db.execute(
                    text("SELECT setval(pg_get_serial_sequence(:table_name, :column_name), 1, false)"),
                    {"table_name": table, "column_name": pk},
                )
        db.commit()
    finally:
        db.close()


def bootstrap_remote_database() -> bool:
    if os.getenv("DATABASE_BOOTSTRAP_FROM_SQLITE", "1").lower() in {"0", "false", "no"}:
        return False
    if IS_SQLITE:
        return False
    if not DATABASE_PATH.exists():
        return False

    target_db = SessionLocal()
    try:
        if any(target_db.query(model).first() for model in (AdminUser, SiteSetting, ContentItem, News, Department, Teacher)):
            return False
    finally:
        target_db.close()

    source_engine = create_engine(
        f"sqlite:///{DATABASE_PATH.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    SourceSession = sessionmaker(autocommit=False, autoflush=False, bind=source_engine)

    source_db = SourceSession()
    target_db = SessionLocal()
    try:
        if not any(source_db.query(model).first() for model in (AdminUser, SiteSetting, ContentItem)):
            return False

        for model in BOOTSTRAP_MODELS:
            rows = source_db.query(model).all()
            for row in rows:
                payload = {column.name: getattr(row, column.name) for column in model.__table__.columns}
                target_db.merge(model(**payload))

        target_db.commit()
        sync_postgres_sequences()
        return True
    finally:
        source_db.close()
        target_db.close()
        source_engine.dispose()

import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from app.database import DATABASE_PATH, IS_SQLITE, SessionLocal, engine
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

SITE_SETTINGS_RUNTIME_COLUMNS = {
    "announcements_header_media_path": "TEXT",
    "announcements_header_media_type": "VARCHAR(20)",
    "teachers_header_media_path": "TEXT",
    "teachers_header_media_type": "VARCHAR(20)",
    "contact_phone_secondary": "TEXT",
    "contact_phone_hotline": "TEXT",
    "contact_hours_uz": "TEXT",
    "contact_hours_en": "TEXT",
    "contact_hours_ru": "TEXT",
}


def ensure_site_settings_schema(target_engine=engine, sqlite_mode: bool | None = None) -> None:
    sqlite_mode = IS_SQLITE if sqlite_mode is None else sqlite_mode
    inspector = inspect(target_engine)

    if "site_settings" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("site_settings")}

    with target_engine.begin() as connection:
        for column_name, column_type in SITE_SETTINGS_RUNTIME_COLUMNS.items():
            if column_name in existing_columns:
                continue

            if sqlite_mode:
                connection.execute(text(f"ALTER TABLE site_settings ADD COLUMN {column_name} {column_type}"))
            else:
                connection.execute(text(f"ALTER TABLE site_settings ADD COLUMN IF NOT EXISTS {column_name} {column_type}"))


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
    ensure_site_settings_schema(source_engine, sqlite_mode=True)
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

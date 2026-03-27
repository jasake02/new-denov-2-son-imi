from sqlalchemy.orm import Session
from app.models.models import ContentItem
from app.services.russian_text import normalize_russian_text

def get_content_translation(db: Session, lang: str, key: str, default_uz: str, default_en: str = None, default_ru: str = None) -> str:
    item = db.query(ContentItem).filter(ContentItem.key == key).first()
    
    if not item:
        # Create it if it doesn't exist
        item = ContentItem(
            key=key,
            value_uz=default_uz,
            value_en=default_en,
            value_ru=normalize_russian_text(default_ru) if default_ru else default_ru
        )
        db.add(item)
        db.commit()
    
    if lang == "en":
        return item.value_en if item.value_en else (default_en or default_uz)
    elif lang == "ru":
        value = item.value_ru if item.value_ru else (default_ru or default_uz)
        return normalize_russian_text(value)
    else:
        return item.value_uz if item.value_uz else default_uz

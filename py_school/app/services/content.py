from sqlalchemy.orm import Session
from app.models.models import ContentItem

def get_content_translation(db: Session, lang: str, key: str, default_uz: str, default_en: str = None, default_ru: str = None) -> str:
    item = db.query(ContentItem).filter(ContentItem.key == key).first()
    
    if not item:
        # Create it if it doesn't exist
        item = ContentItem(
            key=key,
            value_uz=default_uz,
            value_en=default_en,
            value_ru=default_ru
        )
        db.add(item)
        db.commit()
    
    if lang == "en":
        return item.value_en if item.value_en else (default_en or default_uz)
    elif lang == "ru":
        return item.value_ru if item.value_ru else (default_ru or default_uz)
    else:
        return item.value_uz if item.value_uz else default_uz

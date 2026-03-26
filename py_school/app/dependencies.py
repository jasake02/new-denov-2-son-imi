from itsdangerous import URLSafeSerializer

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import SiteSetting
from app.services.content import get_content_translation
from app.services.localization import get_current_language

# Used for cookie session signing
SECRET_KEY = "denov2_super_secret_key_change_in_production"
serializer = URLSafeSerializer(SECRET_KEY)

def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSetting).filter(SiteSetting.id == 1).first()
    return settings

def get_current_admin(request: Request):
    session_cookie = request.cookies.get("admin_session")
    if not session_cookie:
        return None
    try:
        user_id = serializer.loads(session_cookie)
        return user_id
    except:
        return None

def require_admin(request: Request):
    user_id = get_current_admin(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id

# Template context dependency
def get_template_context(request: Request, db: Session = Depends(get_db)):
    lang = get_current_language(request)
    settings = get_settings(db)
    
    def t(key: str, default_uz: str, default_en: str = None, default_ru: str = None):
        return get_content_translation(db, lang, key, default_uz, default_en, default_ru)

    def ml(obj, field: str):
        localized_value = getattr(obj, f"{field}_{lang}", None)
        if localized_value:
            return localized_value
        return getattr(obj, f"{field}_uz", None)

    def sm(field: str, default: str = None):
        if not settings:
            return default
        localized_value = getattr(settings, f"{field}_{lang}", None)
        if localized_value:
            return localized_value
        return getattr(settings, f"{field}_uz", None) or default
        
    return {
        "request": request,
        "lang": lang,
        "settings": settings,
        "t": t,
        "ml": ml,
        "sm": sm,
    }

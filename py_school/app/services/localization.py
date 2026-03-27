from fastapi import Request
from app.services.russian_text import normalize_russian_text

DEFAULT_LANGUAGE = "uz"
VALID_LANGUAGES = ["uz", "en", "ru"]

def get_current_language(request: Request) -> str:
    # Check cookie
    lang = request.cookies.get("SelectedLanguage")
    if lang and lang in VALID_LANGUAGES:
        return lang
    
    # Check Accept-Language header
    accept_lang = request.headers.get("Accept-Language", "")
    if accept_lang:
        preferred = accept_lang.split(",")[0].split("-")[0].lower()
        if preferred in VALID_LANGUAGES:
            return preferred
            
    return DEFAULT_LANGUAGE

def get_text(lang: str, uz: str, en: str, ru: str) -> str:
    if lang == "en" and en:
        return en
    elif lang == "ru" and ru:
        return normalize_russian_text(ru)
    return uz

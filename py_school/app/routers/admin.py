from collections import defaultdict
from datetime import datetime
import os

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.bootstrap import sync_postgres_sequences
from app.database import get_db
from app.dependencies import SECRET_KEY, get_current_admin, require_admin, serializer
from app.models.models import AdminUser, ContentItem, ContactMessage, Department, News, SiteSetting, Teacher
from app.services.auth import get_password_hash, verify_password
from app.services.storage import delete_media, save_upload_file
from app.services.teacher_order import build_effective_order_map, normalize_order_value, sort_teachers_for_display
from app.template_loader import create_templates

router = APIRouter()
templates = create_templates()

ANNOUNCEMENT_CATEGORIES = {"announcement", "agency"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg", ".mov"}
DEPARTMENT_CATEGORY_ALIASES = {"leaders": "leadership", "teachers": "academic", "staff": "support"}
TEACHER_CATEGORY_ALIASES = {
    "leaders": "leadership",
    "teachers": "science",
    "staff": "natural",
    "primary": "natural",
    "practical": "creative",
    "applied": "creative",
    "creative": "creative",
    "arts": "creative",
    "humanities": "humanities",
    "social": "humanities",
    "socials": "humanities",
    "social-humanitarian": "humanities",
}
CONTENT_SECTION_CONFIG = [
    ("nav", "Navbar"),
    ("home", "Bosh sahifa"),
    ("about", "Maktab haqida"),
    ("news", "Yangiliklar"),
    ("announcements", "E'lonlar"),
    ("departments", "Bo'limlar"),
    ("dept", "Bo'lim sahifasi"),
    ("teachers", "Ustozlar"),
    ("teacher", "Ustoz detail"),
    ("contact", "Bog'lanish"),
    ("footer", "Footer"),
    ("general", "Umumiy"),
]
CODE_EDIT_PHRASE = os.getenv("ADMIN_CODE_EDIT_PHRASE") or SECRET_KEY


def redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url=url, status_code=303)


def commit_with_retry(db: Session, pending_obj=None) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        sync_postgres_sequences()
        if pending_obj is not None:
            db.add(pending_obj)
        db.commit()


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def normalize_news_category(value: str | None) -> str:
    if value in ANNOUNCEMENT_CATEGORIES:
        return "announcement"
    return "school"


def normalize_department_category(value: str | None) -> str:
    if not value:
        return "academic"
    return DEPARTMENT_CATEGORY_ALIASES.get(value, value)


def normalize_teacher_category(value: str | None) -> str:
    if not value:
        return "science"
    return TEACHER_CATEGORY_ALIASES.get(value, value)


def detect_media_type(file_path: str | None) -> str | None:
    if not file_path:
        return None
    extension = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    extension = f".{extension}" if extension else ""
    return "video" if extension in VIDEO_EXTENSIONS else "image"


def build_content_sections(items: list[ContentItem]) -> list[dict]:
    grouped: dict[str, list[ContentItem]] = defaultdict(list)
    for item in items:
        section_key = item.key.split(".", 1)[0] if "." in item.key else "general"
        grouped[section_key].append(item)

    sections = []
    used_keys = set()
    for key, title in CONTENT_SECTION_CONFIG:
        section_items = grouped.get(key)
        if not section_items:
            continue
        sections.append({"key": key, "title": title, "items": sorted(section_items, key=lambda item: item.key)})
        used_keys.add(key)

    for key in sorted(grouped.keys() - used_keys):
        sections.append({"key": key, "title": key.replace("_", " ").title(), "items": sorted(grouped[key], key=lambda item: item.key)})

    return sections


def build_teacher_category_order_map(items: list[Teacher]) -> dict[int, int]:
    grouped: dict[str, list[Teacher]] = defaultdict(list)
    for item in items:
        grouped[item.category_key].append(item)

    effective_orders: dict[int, int] = {}
    for teachers in grouped.values():
        effective_orders.update(build_effective_order_map(teachers, mode="category"))
    return effective_orders


def can_edit_code(admin_user: AdminUser | None, submitted_phrase: str | None) -> bool:
    normalized_phrase = normalize_text(submitted_phrase)
    if not normalized_phrase:
        return False
    if admin_user and admin_user.secret_word_hash:
        return verify_password(normalized_phrase, admin_user.secret_word_hash)
    return normalized_phrase == normalize_text(CODE_EDIT_PHRASE)


@router.get("/", response_class=HTMLResponse)
def admin_root(request: Request):
    if get_current_admin(request):
        return redirect("/admin/dashboard")
    return redirect("/admin/login")


@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request, error: str = None):
    if get_current_admin(request):
        return redirect("/admin/dashboard")
    return templates.TemplateResponse(request=request, name="admin/login.html", context={"request": request, "error": error})


@router.post("/login")
def login_post(request: Request, user_name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.user_name == user_name).first()

    if user and verify_password(password, user.password_hash):
        user.last_login = datetime.utcnow()
        db.commit()

        response = redirect("/admin/dashboard")
        session_token = serializer.dumps(user.id)
        response.set_cookie(
            key="admin_session",
            value=session_token,
            httponly=True,
            max_age=86400,
            samesite="lax",
            secure=bool(os.getenv("VERCEL")) or request.url.scheme == "https",
        )
        return response

    return redirect("/admin/login?error=Noto'g'ri login yoki parol")


@router.post("/logout")
def logout():
    response = redirect("/admin/login")
    response.delete_cookie("admin_session")
    return response


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    news_count = db.query(News).filter(~News.category_key.in_(ANNOUNCEMENT_CATEGORIES)).count()
    announcements_count = db.query(News).filter(News.category_key.in_(ANNOUNCEMENT_CATEGORIES)).count()
    departments_count = db.query(Department).count()
    teachers_count = db.query(Teacher).count()
    unread_msgs = db.query(ContactMessage).filter(ContactMessage.is_read == False).count()

    recent_news = db.query(News).order_by(desc(News.created_date)).limit(5).all()
    recent_msgs = db.query(ContactMessage).order_by(desc(ContactMessage.created_date)).limit(5).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "request": request,
            "news_count": news_count,
            "announcements_count": announcements_count,
            "departments_count": departments_count,
            "teachers_count": teachers_count,
            "unread_msgs": unread_msgs,
            "recent_news": recent_news,
            "recent_msgs": recent_msgs,
        },
    )


@router.get("/news", response_class=HTMLResponse)
def admin_news_list(request: Request, kind: str = "all", admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    query = db.query(News).order_by(desc(News.created_date))
    if kind == "news":
        query = query.filter(~News.category_key.in_(ANNOUNCEMENT_CATEGORIES))
    elif kind == "announcement":
        query = query.filter(News.category_key.in_(ANNOUNCEMENT_CATEGORIES))

    return templates.TemplateResponse(
        request=request,
        name="admin/news.html",
        context={"request": request, "items": query.all(), "kind": kind},
    )


@router.post("/news/create")
def admin_news_create(
    request: Request,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    category_key: str = Form("school"),
    title_uz: str = Form(...),
    content_uz: str = Form(...),
    title_en: str = Form(None),
    content_en: str = Form(None),
    title_ru: str = Form(None),
    content_ru: str = Form(None),
    media_file: UploadFile = File(None),
):
    normalized_category = normalize_news_category(category_key)
    image_path = save_upload_file(media_file) if media_file and media_file.filename else None

    item = News(
        title_uz=title_uz.strip(),
        content_uz=content_uz.strip(),
        title_en=normalize_text(title_en),
        content_en=normalize_text(content_en),
        title_ru=normalize_text(title_ru),
        content_ru=normalize_text(content_ru),
        category_key=normalized_category,
        image_path=image_path,
    )
    db.add(item)
    commit_with_retry(db, item)
    kind = "announcement" if normalized_category == "announcement" else "news"
    return redirect(f"/admin/news?kind={kind}")


@router.post("/news/edit/{id}")
def admin_news_edit(
    request: Request,
    id: int,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    category_key: str = Form("school"),
    title_uz: str = Form(...),
    content_uz: str = Form(...),
    title_en: str = Form(None),
    content_en: str = Form(None),
    title_ru: str = Form(None),
    content_ru: str = Form(None),
    media_file: UploadFile = File(None),
):
    item = db.query(News).filter(News.id == id).first()
    if not item:
        return redirect("/admin/news")

    normalized_category = normalize_news_category(category_key)
    item.title_uz = title_uz.strip()
    item.content_uz = content_uz.strip()
    item.title_en = normalize_text(title_en)
    item.content_en = normalize_text(content_en)
    item.title_ru = normalize_text(title_ru)
    item.content_ru = normalize_text(content_ru)
    item.category_key = normalized_category
    item.modified_date = datetime.utcnow()

    if media_file and media_file.filename:
        delete_media(item.image_path)
        item.image_path = save_upload_file(media_file)

    commit_with_retry(db)
    kind = "announcement" if normalized_category == "announcement" else "news"
    return redirect(f"/admin/news?kind={kind}")


@router.post("/news/delete/{id}")
def admin_news_delete(
    request: Request,
    id: int,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    kind: str = Form("all"),
):
    item = db.query(News).filter(News.id == id).first()
    if item:
        delete_media(item.image_path)
        db.delete(item)
        commit_with_retry(db)
    return redirect(f"/admin/news?kind={kind}")


@router.get("/departments", response_class=HTMLResponse)
def admin_departments_list(request: Request, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    items = db.query(Department).order_by(desc(Department.created_date)).all()
    return templates.TemplateResponse(request=request, name="admin/departments.html", context={"request": request, "items": items})


@router.post("/departments/create")
def admin_departments_create(
    request: Request,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    category_key: str = Form("academic"),
    name_uz: str = Form(...),
    description_uz: str = Form(None),
    name_en: str = Form(None),
    description_en: str = Form(None),
    name_ru: str = Form(None),
    description_ru: str = Form(None),
    has_subjects: bool = Form(False),
    subjects_uz: str = Form(None),
    subjects_en: str = Form(None),
    subjects_ru: str = Form(None),
    media_file: UploadFile = File(None),
):
    image_path = save_upload_file(media_file) if media_file and media_file.filename else None

    item = Department(
        name_uz=name_uz.strip(),
        description_uz=normalize_text(description_uz),
        name_en=normalize_text(name_en),
        description_en=normalize_text(description_en),
        name_ru=normalize_text(name_ru),
        description_ru=normalize_text(description_ru),
        category_key=normalize_department_category(category_key),
        has_subjects=has_subjects,
        subjects_uz=normalize_text(subjects_uz) if has_subjects else None,
        subjects_en=normalize_text(subjects_en) if has_subjects else None,
        subjects_ru=normalize_text(subjects_ru) if has_subjects else None,
        image_path=image_path,
    )
    db.add(item)
    commit_with_retry(db, item)
    return redirect("/admin/departments")


@router.post("/departments/edit/{id}")
def admin_departments_edit(
    request: Request,
    id: int,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    category_key: str = Form("academic"),
    name_uz: str = Form(...),
    description_uz: str = Form(None),
    name_en: str = Form(None),
    description_en: str = Form(None),
    name_ru: str = Form(None),
    description_ru: str = Form(None),
    has_subjects: bool = Form(False),
    subjects_uz: str = Form(None),
    subjects_en: str = Form(None),
    subjects_ru: str = Form(None),
    media_file: UploadFile = File(None),
):
    item = db.query(Department).filter(Department.id == id).first()
    if not item:
        return redirect("/admin/departments")

    item.name_uz = name_uz.strip()
    item.description_uz = normalize_text(description_uz)
    item.name_en = normalize_text(name_en)
    item.description_en = normalize_text(description_en)
    item.name_ru = normalize_text(name_ru)
    item.description_ru = normalize_text(description_ru)
    item.category_key = normalize_department_category(category_key)
    item.has_subjects = has_subjects
    item.subjects_uz = normalize_text(subjects_uz) if has_subjects else None
    item.subjects_en = normalize_text(subjects_en) if has_subjects else None
    item.subjects_ru = normalize_text(subjects_ru) if has_subjects else None
    item.modified_date = datetime.utcnow()

    if media_file and media_file.filename:
        delete_media(item.image_path)
        item.image_path = save_upload_file(media_file)

    commit_with_retry(db)
    return redirect("/admin/departments")


@router.post("/departments/delete/{id}")
def admin_departments_delete(request: Request, id: int, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    item = db.query(Department).filter(Department.id == id).first()
    if item:
        delete_media(item.image_path)
        db.delete(item)
        commit_with_retry(db)
    return redirect("/admin/departments")


@router.get("/teachers", response_class=HTMLResponse)
def admin_teachers_list(request: Request, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    items = db.query(Teacher).all()
    sorted_items = sort_teachers_for_display(items, mode="all")
    return templates.TemplateResponse(
        request=request,
        name="admin/teachers.html",
        context={
            "request": request,
            "items": sorted_items,
            "all_order_map": build_effective_order_map(sorted_items, mode="all"),
            "category_order_map": build_teacher_category_order_map(items),
        },
    )


@router.post("/teachers/create")
def admin_teachers_create(
    request: Request,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: str = Form(None),
    category_key: str = Form("science"),
    display_order: str = Form(None),
    category_display_order: str = Form(None),
    position_uz: str = Form(None),
    position_en: str = Form(None),
    position_ru: str = Form(None),
    subject_uz: str = Form(None),
    subject_en: str = Form(None),
    subject_ru: str = Form(None),
    bio_uz: str = Form(None),
    bio_en: str = Form(None),
    bio_ru: str = Form(None),
    achievements_uz: str = Form(None),
    achievements_en: str = Form(None),
    achievements_ru: str = Form(None),
    media_file: UploadFile = File(None),
):
    image_path = save_upload_file(media_file) if media_file and media_file.filename else None

    item = Teacher(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        middle_name=normalize_text(middle_name),
        category_key=normalize_teacher_category(category_key),
        display_order=normalize_order_value(display_order),
        category_display_order=normalize_order_value(category_display_order),
        position_uz=normalize_text(position_uz),
        position_en=normalize_text(position_en),
        position_ru=normalize_text(position_ru),
        subject_uz=normalize_text(subject_uz),
        subject_en=normalize_text(subject_en),
        subject_ru=normalize_text(subject_ru),
        bio_uz=normalize_text(bio_uz),
        bio_en=normalize_text(bio_en),
        bio_ru=normalize_text(bio_ru),
        achievements_uz=normalize_text(achievements_uz),
        achievements_en=normalize_text(achievements_en),
        achievements_ru=normalize_text(achievements_ru),
        image_path=image_path,
    )
    db.add(item)
    commit_with_retry(db, item)
    return redirect("/admin/teachers")


@router.post("/teachers/edit/{id}")
def admin_teachers_edit(
    request: Request,
    id: int,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: str = Form(None),
    category_key: str = Form("science"),
    display_order: str = Form(None),
    category_display_order: str = Form(None),
    position_uz: str = Form(None),
    position_en: str = Form(None),
    position_ru: str = Form(None),
    subject_uz: str = Form(None),
    subject_en: str = Form(None),
    subject_ru: str = Form(None),
    bio_uz: str = Form(None),
    bio_en: str = Form(None),
    bio_ru: str = Form(None),
    achievements_uz: str = Form(None),
    achievements_en: str = Form(None),
    achievements_ru: str = Form(None),
    media_file: UploadFile = File(None),
):
    item = db.query(Teacher).filter(Teacher.id == id).first()
    if not item:
        return redirect("/admin/teachers")

    item.first_name = first_name.strip()
    item.last_name = last_name.strip()
    item.middle_name = normalize_text(middle_name)
    item.category_key = normalize_teacher_category(category_key)
    item.display_order = normalize_order_value(display_order)
    item.category_display_order = normalize_order_value(category_display_order)
    item.position_uz = normalize_text(position_uz)
    item.position_en = normalize_text(position_en)
    item.position_ru = normalize_text(position_ru)
    item.subject_uz = normalize_text(subject_uz)
    item.subject_en = normalize_text(subject_en)
    item.subject_ru = normalize_text(subject_ru)
    item.bio_uz = normalize_text(bio_uz)
    item.bio_en = normalize_text(bio_en)
    item.bio_ru = normalize_text(bio_ru)
    item.achievements_uz = normalize_text(achievements_uz)
    item.achievements_en = normalize_text(achievements_en)
    item.achievements_ru = normalize_text(achievements_ru)
    item.modified_date = datetime.utcnow()

    if media_file and media_file.filename:
        delete_media(item.image_path)
        item.image_path = save_upload_file(media_file)

    commit_with_retry(db)
    return redirect("/admin/teachers")


@router.post("/teachers/delete/{id}")
def admin_teachers_delete(request: Request, id: int, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    item = db.query(Teacher).filter(Teacher.id == id).first()
    if item:
        delete_media(item.image_path)
        db.delete(item)
        commit_with_retry(db)
    return redirect("/admin/teachers")


@router.get("/account/changepassword", response_class=HTMLResponse)
def change_pwd_get(request: Request, admin_id: int = Depends(require_admin), success: str = None, error: str = None):
    return templates.TemplateResponse(
        request=request,
        name="admin/changepassword.html",
        context={"request": request, "success": success, "error": error},
    )


@router.post("/account/changepassword")
def change_pwd_post(
    request: Request,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    old_password: str = Form(...),
    code_phrase: str = Form(...),
    new_password: str = Form(...),
):
    user = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    if not user or not verify_password(old_password, user.password_hash):
        return redirect("/admin/account/changepassword?error=Eski parol noto'g'ri")

    if not can_edit_code(user, code_phrase):
        return redirect("/admin/account/changepassword?error=Maxsus so'z noto'g'ri")

    if len(new_password.strip()) < 8:
        return redirect("/admin/account/changepassword?error=Yangi parol kamida 8 ta belgidan iborat bo'lsin")

    user.password_hash = get_password_hash(new_password)
    commit_with_retry(db)
    return redirect("/admin/account/changepassword?success=Parol muvaffaqiyatli o'zgartirildi")


@router.get("/messages", response_class=HTMLResponse)
def admin_messages_list(request: Request, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    items = db.query(ContactMessage).order_by(desc(ContactMessage.created_date)).all()
    unread = db.query(ContactMessage).filter(ContactMessage.is_read == False).all()
    for message in unread:
        message.is_read = True
    if unread:
        commit_with_retry(db)
    return templates.TemplateResponse(request=request, name="admin/messages.html", context={"request": request, "items": items})


@router.post("/messages/delete/{id}")
def admin_messages_delete(request: Request, id: int, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    item = db.query(ContactMessage).filter(ContactMessage.id == id).first()
    if item:
        db.delete(item)
        commit_with_retry(db)
    return redirect("/admin/messages")


@router.get("/sitesettings", response_class=HTMLResponse)
def admin_settings_get(
    request: Request,
    saved: int = 0,
    code_locked: int = 0,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
):
    settings = db.query(SiteSetting).first()
    if not settings:
        settings = SiteSetting(id=1)
        db.add(settings)
        commit_with_retry(db)
        db.refresh(settings)
    return templates.TemplateResponse(
        request=request,
        name="admin/settings.html",
        context={"request": request, "settings": settings, "saved": bool(saved), "code_locked": bool(code_locked)},
    )


@router.post("/sitesettings")
async def admin_settings_post(request: Request, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    settings = db.query(SiteSetting).first()
    admin_user = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    if not settings:
        settings = SiteSetting(id=1)
        db.add(settings)

    form = await request.form()
    previous_custom_css = normalize_text(settings.custom_css)
    submitted_custom_css = normalize_text(form.get("custom_css"))
    code_changed = submitted_custom_css != previous_custom_css

    text_fields = [
        "school_name_uz",
        "school_name_en",
        "school_name_ru",
        "nav_home_uz",
        "nav_home_en",
        "nav_home_ru",
        "nav_about_uz",
        "nav_about_en",
        "nav_about_ru",
        "nav_news_uz",
        "nav_news_en",
        "nav_news_ru",
        "nav_departments_uz",
        "nav_departments_en",
        "nav_departments_ru",
        "nav_contact_uz",
        "nav_contact_en",
        "nav_contact_ru",
        "navbar_bg_color",
        "navbar_text_color",
        "navbar_hover_color",
        "primary_color",
        "primary_dark_color",
        "accent_color",
        "body_bg_color",
        "hero_title_uz",
        "hero_title_en",
        "hero_title_ru",
        "hero_subtitle_uz",
        "hero_subtitle_en",
        "hero_subtitle_ru",
        "about_title_uz",
        "about_title_en",
        "about_title_ru",
        "about_description_uz",
        "about_description_en",
        "about_description_ru",
        "footer_map_embed_url",
        "footer_address_uz",
        "footer_address_en",
        "footer_address_ru",
        "footer_phone",
        "contact_phone_secondary",
        "contact_phone_hotline",
        "contact_hours_uz",
        "contact_hours_en",
        "contact_hours_ru",
        "footer_email",
        "footer_bg_color",
        "footer_text_color",
        "facebook_url",
        "telegram_url",
        "instagram_url",
    ]

    for field_name in text_fields:
        setattr(settings, field_name, normalize_text(form.get(field_name)))

    upload_fields = {
        "navbar_logo_file": "navbar_logo_path",
        "favicon_file": "favicon_path",
        "hero_media_file": "hero_media_path",
        "about_image_file": "about_image_path",
        "about_header_media_file": "about_header_media_path",
        "news_header_media_file": "news_header_media_path",
        "announcements_header_media_file": "announcements_header_media_path",
        "departments_header_media_file": "departments_header_media_path",
        "teachers_header_media_file": "teachers_header_media_path",
        "contact_header_media_file": "contact_header_media_path",
    }

    for upload_name, target_attr in upload_fields.items():
        upload = form.get(upload_name)
        if upload and getattr(upload, "filename", ""):
            delete_media(getattr(settings, target_attr))
            saved_path = save_upload_file(upload)
            setattr(settings, target_attr, saved_path)

            media_type_attr = target_attr.replace("_path", "_type")
            if hasattr(settings, media_type_attr):
                setattr(settings, media_type_attr, detect_media_type(saved_path))

    code_locked = False
    if code_changed:
        if can_edit_code(admin_user, form.get("code_edit_phrase")):
            settings.custom_css = submitted_custom_css
        else:
            code_locked = True

    commit_with_retry(db)
    next_url = "/admin/sitesettings?saved=1"
    if code_locked:
        next_url += "&code_locked=1"
    return redirect(next_url)


@router.get("/content", response_class=HTMLResponse)
def admin_content_get(request: Request, admin_id: int = Depends(require_admin), db: Session = Depends(get_db)):
    items = db.query(ContentItem).order_by(ContentItem.key).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/content.html",
        context={"request": request, "items": items, "sections": build_content_sections(items)},
    )


@router.post("/content/create")
def admin_content_create(
    request: Request,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    key: str = Form(...),
    value_uz: str = Form(...),
    value_en: str = Form(None),
    value_ru: str = Form(None),
):
    normalized_key = key.strip()
    if not db.query(ContentItem).filter(ContentItem.key == normalized_key).first():
        db.add(
            ContentItem(
                key=normalized_key,
                value_uz=value_uz.strip(),
                value_en=normalize_text(value_en),
                value_ru=normalize_text(value_ru),
            )
        )
        commit_with_retry(db)
    return redirect("/admin/content")


@router.post("/content/edit/{id}")
def admin_content_post(
    request: Request,
    id: int,
    admin_id: int = Depends(require_admin),
    db: Session = Depends(get_db),
    value_uz: str = Form(...),
    value_en: str = Form(None),
    value_ru: str = Form(None),
):
    item = db.query(ContentItem).filter(ContentItem.id == id).first()
    if item:
        item.value_uz = value_uz.strip()
        item.value_en = normalize_text(value_en)
        item.value_ru = normalize_text(value_ru)
        commit_with_retry(db)
    return redirect("/admin/content")


@router.get("/{path:path}")
def admin_catch_all(request: Request, path: str, admin_id: int = Depends(require_admin)):
    return HTMLResponse(f"<h3>Admin - {path.capitalize()} is under construction...</h3><br><a href='/admin/dashboard'>Go back</a>")

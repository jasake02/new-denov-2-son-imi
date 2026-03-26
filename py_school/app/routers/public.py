from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import STATIC_DIR, get_db
from app.dependencies import get_template_context
from app.models.models import ContactMessage, Department, News, Teacher
from app.template_loader import create_templates

router = APIRouter()
templates = create_templates()

ANNOUNCEMENT_CATEGORIES = ("announcement", "agency")
DEPARTMENT_CATEGORY_ALIASES = {"leaders": "leadership", "teachers": "academic", "staff": "support"}
TEACHER_CATEGORY_ALIASES = {"leaders": "leadership", "teachers": "science", "staff": "natural", "primary": "natural"}


def normalize_public_category(value: str, aliases: dict[str, str]) -> str:
    return aliases.get(value, value)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    context = get_template_context(request, db)

    latest_news = (
        db.query(News)
        .filter(~News.category_key.in_(ANNOUNCEMENT_CATEGORIES))
        .order_by(desc(News.created_date))
        .limit(3)
        .all()
    )
    latest_announcements = (
        db.query(News)
        .filter(News.category_key.in_(ANNOUNCEMENT_CATEGORIES))
        .order_by(desc(News.created_date))
        .limit(3)
        .all()
    )
    featured_departments = db.query(Department).order_by(desc(Department.created_date)).limit(3).all()
    featured_teachers = (
        db.query(Teacher)
        .order_by(Teacher.display_order.asc(), Teacher.last_name.asc(), Teacher.first_name.asc())
        .limit(4)
        .all()
    )

    context.update(
        {
            "latest_news": latest_news,
            "latest_announcements": latest_announcements,
            "featured_departments": featured_departments,
            "featured_teachers": featured_teachers,
            "teachers_count": db.query(Teacher).count(),
            "announcements_count": db.query(News).filter(News.category_key.in_(ANNOUNCEMENT_CATEGORIES)).count(),
            "departments_count": db.query(Department).count(),
            "news_count": db.query(News).filter(~News.category_key.in_(ANNOUNCEMENT_CATEGORIES)).count(),
        }
    )

    return templates.TemplateResponse(request=request, name="public/index.html", context=context)


@router.get("/about", response_class=HTMLResponse)
def about(request: Request, db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    return templates.TemplateResponse(request=request, name="public/about.html", context=context)


@router.get("/news", response_class=HTMLResponse)
def news_list(request: Request, category: str = "all", db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    category = "announcement" if category == "agency" else category

    query = db.query(News).order_by(desc(News.created_date))
    if category == "announcement":
        query = query.filter(News.category_key.in_(ANNOUNCEMENT_CATEGORIES))
    elif category != "all":
        query = query.filter(News.category_key == category)

    context.update({"news_list": query.all(), "category": category})
    return templates.TemplateResponse(request=request, name="public/news.html", context=context)


@router.get("/news/{news_id}", response_class=HTMLResponse)
def news_detail(request: Request, news_id: int, db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return RedirectResponse(url="/news", status_code=303)

    context.update({"news": news})
    return templates.TemplateResponse(request=request, name="public/news_detail.html", context=context)


@router.get("/announcements", response_class=HTMLResponse)
def announcements_list(request: Request, db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    items = (
        db.query(News)
        .filter(News.category_key.in_(ANNOUNCEMENT_CATEGORIES))
        .order_by(desc(News.created_date))
        .all()
    )
    context.update({"announcements": items})
    return templates.TemplateResponse(request=request, name="public/announcements.html", context=context)


@router.get("/departments", response_class=HTMLResponse)
def departments_list(request: Request, category: str = "all", db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    category = normalize_public_category(category, DEPARTMENT_CATEGORY_ALIASES)
    query = db.query(Department).order_by(desc(Department.created_date))
    if category != "all":
        query = query.filter(Department.category_key == category)
    context.update({"departments": query.all(), "category": category})
    return templates.TemplateResponse(request=request, name="public/departments.html", context=context)


@router.get("/departments/{dept_id}", response_class=HTMLResponse)
def department_detail(request: Request, dept_id: int, db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    department = db.query(Department).filter(Department.id == dept_id).first()
    if not department:
        return RedirectResponse(url="/departments", status_code=303)

    context.update({"dept": department})
    return templates.TemplateResponse(request=request, name="public/department_detail.html", context=context)


@router.get("/teachers", response_class=HTMLResponse)
def teachers_list(request: Request, category: str = "all", db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    category = normalize_public_category(category, TEACHER_CATEGORY_ALIASES)
    query = db.query(Teacher).order_by(Teacher.display_order.asc(), Teacher.last_name.asc(), Teacher.first_name.asc())
    if category != "all":
        query = query.filter(Teacher.category_key == category)
    context.update({"teachers": query.all(), "category": category})
    return templates.TemplateResponse(request=request, name="public/teachers.html", context=context)


@router.get("/teachers/{teacher_id}", response_class=HTMLResponse)
def teacher_detail(request: Request, teacher_id: int, db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        return RedirectResponse(url="/teachers", status_code=303)

    related_teachers = (
        db.query(Teacher)
        .filter(Teacher.id != teacher.id, Teacher.category_key == teacher.category_key)
        .order_by(Teacher.display_order.asc(), Teacher.last_name.asc(), Teacher.first_name.asc())
        .limit(3)
        .all()
    )
    context.update({"teacher": teacher, "related_teachers": related_teachers})
    return templates.TemplateResponse(request=request, name="public/teacher_detail.html", context=context)


@router.get("/contact", response_class=HTMLResponse)
def contact_get(request: Request, success: bool = False, db: Session = Depends(get_db)):
    context = get_template_context(request, db)
    context.update({"success": success})
    return templates.TemplateResponse(request=request, name="public/contact.html", context=context)


@router.post("/contact")
def contact_post(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    clean_message = BeautifulSoup(message, "html.parser").get_text()

    new_message = ContactMessage(full_name=full_name, email=email, message=clean_message)
    db.add(new_message)
    db.commit()

    context = get_template_context(request, db)
    context.update({"success": True})
    return templates.TemplateResponse(request=request, name="public/contact.html", context=context)


@router.get("/lang/{lang_code}")
def change_language(lang_code: str, next: str = "/"):
    if lang_code not in ["uz", "en", "ru"]:
        lang_code = "uz"

    response = RedirectResponse(url=next)
    response.set_cookie(key="SelectedLanguage", value=lang_code, max_age=31536000, httponly=False)
    return response


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    return "User-agent: *\nAllow: /\nSitemap: /sitemap.xml"


@router.get("/favicon.ico", include_in_schema=False)
def favicon_ico():
    favicon_path = STATIC_DIR / "images" / "ptma-01.png"
    if favicon_path.exists():
        return FileResponse(favicon_path, media_type="image/png")
    return RedirectResponse(url="/static/images/PIIMALogo.svg", status_code=307)


@router.get("/favicon.png", include_in_schema=False)
def favicon_png():
    favicon_path = STATIC_DIR / "images" / "ptma-01.png"
    if favicon_path.exists():
        return FileResponse(favicon_path, media_type="image/png")
    return RedirectResponse(url="/static/images/PIIMALogo.svg", status_code=307)


@router.get("/sitemap.xml", response_class=PlainTextResponse)
def sitemap_xml(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    pages = ["", "/about", "/news", "/announcements", "/departments", "/teachers", "/contact"]
    for page in pages:
        xml.append(f"  <url><loc>{base_url}{page}</loc></url>")

    for news in db.query(News).all():
        xml.append(f"  <url><loc>{base_url}/news/{news.id}</loc></url>")

    for department in db.query(Department).all():
        xml.append(f"  <url><loc>{base_url}/departments/{department.id}</loc></url>")

    for teacher in db.query(Teacher).all():
        xml.append(f"  <url><loc>{base_url}/teachers/{teacher.id}</loc></url>")

    xml.append("</urlset>")
    return "\n".join(xml)

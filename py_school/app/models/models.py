from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String, nullable=True) # Used initially then empty
    password_hash = Column(String, nullable=True)
    secret_word_hash = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Uzbek Content
    name_uz = Column(String(150), nullable=False)
    description_uz = Column(Text, nullable=True)
    
    # English Content
    name_en = Column(String(150), nullable=True)
    description_en = Column(Text, nullable=True)
    
    # Russian Content
    name_ru = Column(String(150), nullable=True)
    description_ru = Column(Text, nullable=True)
    
    # Image & Metadata
    image_path = Column(String, nullable=True)
    category_key = Column(String(50), default="academic")
    
    has_subjects = Column(Boolean, default=False)
    subjects_uz = Column(Text, nullable=True)
    subjects_en = Column(Text, nullable=True)
    subjects_ru = Column(Text, nullable=True)
    
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, nullable=True)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    
    # Uzbek Content
    title_uz = Column(String(200), nullable=False)
    content_uz = Column(Text, nullable=False)
    
    # English Content
    title_en = Column(String(200), nullable=True)
    content_en = Column(Text, nullable=True)
    
    # Russian Content
    title_ru = Column(String(200), nullable=True)
    content_ru = Column(Text, nullable=True)
    
    # Image & Metadata
    image_path = Column(String, nullable=True)
    category_key = Column(String(50), default="school")
    
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, nullable=True)


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    middle_name = Column(String(80), nullable=True)

    position_uz = Column(String(150), nullable=True)
    position_en = Column(String(150), nullable=True)
    position_ru = Column(String(150), nullable=True)

    subject_uz = Column(String(150), nullable=True)
    subject_en = Column(String(150), nullable=True)
    subject_ru = Column(String(150), nullable=True)

    bio_uz = Column(Text, nullable=True)
    bio_en = Column(Text, nullable=True)
    bio_ru = Column(Text, nullable=True)

    achievements_uz = Column(Text, nullable=True)
    achievements_en = Column(Text, nullable=True)
    achievements_ru = Column(Text, nullable=True)

    image_path = Column(String, nullable=True)
    category_key = Column(String(50), default="teachers")
    display_order = Column(Integer, default=0)

    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, nullable=True)


class SiteSetting(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    school_name_uz = Column(String, nullable=True)
    school_name_en = Column(String, nullable=True)
    school_name_ru = Column(String, nullable=True)

    navbar_logo_path = Column(String, nullable=True)
    favicon_path = Column(String, nullable=True)
    navbar_bg_color = Column(String, nullable=True)
    navbar_text_color = Column(String, nullable=True)
    navbar_hover_color = Column(String, nullable=True)

    nav_home_uz = Column(String, nullable=True)
    nav_home_en = Column(String, nullable=True)
    nav_home_ru = Column(String, nullable=True)
    nav_about_uz = Column(String, nullable=True)
    nav_about_en = Column(String, nullable=True)
    nav_about_ru = Column(String, nullable=True)
    nav_news_uz = Column(String, nullable=True)
    nav_news_en = Column(String, nullable=True)
    nav_news_ru = Column(String, nullable=True)
    nav_departments_uz = Column(String, nullable=True)
    nav_departments_en = Column(String, nullable=True)
    nav_departments_ru = Column(String, nullable=True)
    nav_contact_uz = Column(String, nullable=True)
    nav_contact_en = Column(String, nullable=True)
    nav_contact_ru = Column(String, nullable=True)

    primary_color = Column(String, nullable=True)
    primary_dark_color = Column(String, nullable=True)
    accent_color = Column(String, nullable=True)
    body_bg_color = Column(String, nullable=True)

    hero_media_path = Column(String, nullable=True)
    hero_media_type = Column(String, nullable=True)
    hero_title_uz = Column(String, nullable=True)
    hero_title_en = Column(String, nullable=True)
    hero_title_ru = Column(String, nullable=True)
    hero_subtitle_uz = Column(String, nullable=True)
    hero_subtitle_en = Column(String, nullable=True)
    hero_subtitle_ru = Column(String, nullable=True)

    about_image_path = Column(String, nullable=True)
    about_header_media_path = Column(String, nullable=True)
    about_header_media_type = Column(String, nullable=True)
    news_header_media_path = Column(String, nullable=True)
    news_header_media_type = Column(String, nullable=True)
    announcements_header_media_path = Column(String, nullable=True)
    announcements_header_media_type = Column(String, nullable=True)
    departments_header_media_path = Column(String, nullable=True)
    departments_header_media_type = Column(String, nullable=True)
    teachers_header_media_path = Column(String, nullable=True)
    teachers_header_media_type = Column(String, nullable=True)
    contact_header_media_path = Column(String, nullable=True)
    contact_header_media_type = Column(String, nullable=True)
    
    about_title_uz = Column(String, nullable=True)
    about_title_en = Column(String, nullable=True)
    about_title_ru = Column(String, nullable=True)
    about_description_uz = Column(Text, nullable=True)
    about_description_en = Column(Text, nullable=True)
    about_description_ru = Column(Text, nullable=True)

    footer_map_embed_url = Column(Text, nullable=True)
    footer_address_uz = Column(String, nullable=True)
    footer_address_en = Column(String, nullable=True)
    footer_address_ru = Column(String, nullable=True)
    footer_phone = Column(String, nullable=True)
    contact_phone_secondary = Column(String, nullable=True)
    contact_phone_hotline = Column(String, nullable=True)
    contact_hours_uz = Column(String, nullable=True)
    contact_hours_en = Column(String, nullable=True)
    contact_hours_ru = Column(String, nullable=True)
    footer_email = Column(String, nullable=True)
    footer_bg_color = Column(String, nullable=True)
    footer_text_color = Column(String, nullable=True)

    facebook_url = Column(String, nullable=True)
    telegram_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)

    custom_css = Column(Text, nullable=True)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value_uz = Column(Text, nullable=True)
    value_en = Column(Text, nullable=True)
    value_ru = Column(Text, nullable=True)

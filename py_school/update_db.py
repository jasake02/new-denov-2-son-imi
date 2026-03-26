import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import SiteSetting, Department
from app.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db = Session()

# 1. Update Settings
settings = db.query(SiteSetting).first()
if settings:
    # Nav
    settings.nav_home_uz = settings.nav_home_uz or "Bosh sahifa"
    settings.nav_home_en = settings.nav_home_en or "Home"
    settings.nav_home_ru = settings.nav_home_ru or "Glavnaya"
    
    settings.nav_about_uz = settings.nav_about_uz or "Maktab haqida"
    settings.nav_about_en = settings.nav_about_en or "About"
    settings.nav_about_ru = settings.nav_about_ru or "O shkole"
    
    settings.nav_news_uz = settings.nav_news_uz or "Yangiliklar"
    settings.nav_news_en = settings.nav_news_en or "News"
    settings.nav_news_ru = settings.nav_news_ru or "Novosti"
    
    # Rename Departments to Teachers in Naval
    settings.nav_departments_uz = "Ustozlar"
    settings.nav_departments_en = "Teachers"
    settings.nav_departments_ru = "Uchitelya"
    
    settings.nav_contact_uz = settings.nav_contact_uz or "Bog'lanish"
    settings.nav_contact_en = settings.nav_contact_en or "Contact"
    settings.nav_contact_ru = settings.nav_contact_ru or "Kontakty"
    
    # Hero
    settings.hero_title_uz = settings.hero_title_uz or "Kelajak sari yorqin qadamlar"
    settings.hero_title_en = settings.hero_title_en or "Bright Steps to the Future"
    settings.hero_title_ru = settings.hero_title_ru or "Yarkie shagi v budushchee"
    
    settings.hero_subtitle_uz = settings.hero_subtitle_uz or "Sifatli ta'lim - farovon kelajak kafolati"
    settings.hero_subtitle_en = settings.hero_subtitle_en or "Quality education - guarantee of a prosperous future"
    settings.hero_subtitle_ru = settings.hero_subtitle_ru or "Kachestvennoye obrazovaniye - zalog blagopoluchnogo budushchego"
    
    # About
    settings.about_title_uz = settings.about_title_uz or "Zamonaviy ta'lim standarti"
    settings.about_title_en = settings.about_title_en or "Modern Education Standard"
    settings.about_title_ru = settings.about_title_ru or "Sovremennyy standart obrazovaniya"
    
    settings.about_description_uz = settings.about_description_uz or "Maktabimiz o'quvchilarga chuqur bilim berish va ularning iqtidorlarini rivojlantirishga qaratilgan eng so'nggi va zamonaviy ta'lim uslublarini joriy etadi."
    settings.about_description_en = settings.about_description_en or "Our school implements the latest and modern educational methods aimed at providing deep knowledge to students and developing their talents."
    settings.about_description_ru = settings.about_description_ru or "Nasha shkola vnedryayet noveyshiye i sovremennyye obrazovatel'nyye metody, napravlennyye na predostavleniye glubokikh znaniy uchashchimsya."

# 2. Update Departments data to Teachers data
departments = db.query(Department).all()
for dep in departments:
    if dep.name_uz == "Tabiiy Fanlar":
        dep.name_uz = "Matematika fanlari ustozi"
        dep.description_uz = "Oliy toifali matematika va fizika o'qituvchisi"
    elif dep.name_uz == "Riyoziyat va Informatika":
        dep.name_uz = "Ingliz tili fani ustozi"
        dep.description_uz = "CEFR C1 darajasiga ega xalqaro toifadagi ustoz"
    elif dep.name_uz == "Til va Literatura":
        dep.name_uz = "Ona tili va adabiyot ustozi"
        dep.description_uz = "O'zbek tili va adabiyot darslarida ixtisoslashgan"

db.commit()
db.close()
print("Database updated successfully!")

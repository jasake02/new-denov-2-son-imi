from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.models import AdminUser, ContentItem, Department, News, SiteSetting, Teacher
from app.services.auth import get_password_hash


def init_db(db: Session):
    settings = db.query(SiteSetting).filter(SiteSetting.id == 1).first()
    if not settings:
        settings = SiteSetting(
            id=1,
            school_name_uz="Denov 2-son ixtisoslashtirilgan maktab",
            school_name_en="Denov 2 Specialized School",
            school_name_ru="Denov 2 School",
            navbar_logo_path="/static/images/piima-logo.svg",
            favicon_path="/static/images/PIIMALogo.svg",
            navbar_bg_color="#1e293b",
            navbar_text_color="#ffffff",
            navbar_hover_color="#facc15",
            nav_home_uz="Bosh sahifa",
            nav_home_en="Home",
            nav_home_ru="Glavnaya",
            nav_about_uz="Maktab haqida",
            nav_about_en="About",
            nav_about_ru="O shkole",
            nav_news_uz="Yangiliklar",
            nav_news_en="News",
            nav_news_ru="Novosti",
            nav_departments_uz="Bo'limlar",
            nav_departments_en="Departments",
            nav_departments_ru="Otdely",
            nav_contact_uz="Bog'lanish",
            nav_contact_en="Contact",
            nav_contact_ru="Kontakty",
            primary_color="#1e293b",
            primary_dark_color="#0f172a",
            accent_color="#0ea5e9",
            body_bg_color="#ffffff",
            hero_media_path="/static/images/boshekranvideo.mp4",
            hero_media_type="video",
            hero_title_uz="Denov tuman 2-son ixtisoslashtirilgan maktab-internati",
            about_image_path="/static/images/maktab haqida.jpg",
            about_header_media_type="image",
            news_header_media_type="image",
            departments_header_media_type="image",
            contact_header_media_type="image",
            footer_map_embed_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3725.98056908652!2d67.90785499227883!3d38.25250913944837!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38b51156e450102f%3A0x60ba697500c44816!2sDenov%202-sonli%20ixtisoslashtirilgan%20maktab%20internati!5e0!3m2!1sen!2s!4v1771743026788!5m2!1sen!2s",
            footer_address_uz="Denov shahar, Surxandaryo viloyati",
            footer_address_en="Denov city, Surxandarya region",
            footer_address_ru="Denov, Surxandarya",
            footer_phone="+998-76-228-25-64",
            contact_phone_secondary="+998-90-123-45-67",
            contact_phone_hotline="+998-99-777-77-77",
            contact_hours_uz="Dushanba - Shanba: 08:00 - 18:00",
            contact_hours_en="Monday - Saturday: 08:00 - 18:00",
            contact_hours_ru="Ponedelnik - Subbota: 08:00 - 18:00",
            footer_email="info@denov2sonimi.uz",
            footer_bg_color="#111827",
            footer_text_color="#e5e7eb",
            facebook_url="https://www.facebook.com/profile.php?id=100086570118090",
            telegram_url="https://t.me/tadbirptmadenov2",
            instagram_url="https://instagram.com/ptmadenov2imi?igshid=YmMyMTA2M2Y=",
        )
        db.add(settings)
    else:
        if not settings.nav_departments_uz or settings.nav_departments_uz == "Ustozlar":
            settings.nav_departments_uz = "Bo'limlar"
        if not settings.nav_departments_en or settings.nav_departments_en == "Teachers":
            settings.nav_departments_en = "Departments"
        if not settings.nav_departments_ru or settings.nav_departments_ru == "Uchitelya":
            settings.nav_departments_ru = "Otdely"
        if not settings.hero_title_uz or settings.hero_title_uz == "Kelajak sari yorqin qadamlar":
            settings.hero_title_uz = "Denov tuman 2-son ixtisoslashtirilgan maktab-internati"
        if not settings.contact_phone_secondary:
            settings.contact_phone_secondary = settings.footer_phone
        if not settings.contact_phone_hotline:
            settings.contact_phone_hotline = settings.footer_phone
        if not settings.contact_hours_uz:
            settings.contact_hours_uz = "Dushanba - Shanba: 08:00 - 18:00"
        if not settings.contact_hours_en:
            settings.contact_hours_en = "Monday - Saturday: 08:00 - 18:00"
        if not settings.contact_hours_ru:
            settings.contact_hours_ru = "Ponedelnik - Subbota: 08:00 - 18:00"

    admin = db.query(AdminUser).filter(AdminUser.is_active == True).first()
    if not admin:
        admin = AdminUser(
            user_name="d2_owner_7824",
            password_hash=get_password_hash("D2s!Admin#2026X"),
            secret_word_hash=get_password_hash("Denov2-Reset@Key"),
        )
        db.add(admin)
    elif not admin.secret_word_hash:
        admin.secret_word_hash = get_password_hash("Denov2-Reset@Key")

    def ensure_content(key: str, uz: str, en: str, ru: str):
        if not db.query(ContentItem).filter(ContentItem.key == key).first():
            db.add(ContentItem(key=key, value_uz=uz, value_en=en, value_ru=ru))

    def upsert_content(key: str, uz: str, en: str, ru: str):
        item = db.query(ContentItem).filter(ContentItem.key == key).first()
        if not item:
            db.add(ContentItem(key=key, value_uz=uz, value_en=en, value_ru=ru))
            return
        item.value_uz = uz
        item.value_en = en
        item.value_ru = ru

    ensure_content("about.mission_vision.title", "Missiyamiz va ko'z qarashimiz", "Our mission and vision", "Nasha missiya i vzglyad")
    ensure_content("about.section.label", "Biz haqimizda", "About us", "O nas")
    ensure_content("about.mission.title", "Missionimiz", "Our mission", "Nasha missiya")
    ensure_content("about.vision.title", "Ko'z qarashimiz", "Our vision", "Nash vzglyad")
    ensure_content("about.mission.description", "Sifatli ta'lim orqali jamiyatga foyda keltirish.", "Serving society through quality education.", "Sluzheniye obshchestvu cherez kachestvennoye obrazovaniye.")
    ensure_content("about.vision.description", "Raqamli asrda yetakchi kadrlar tayyorlash.", "Preparing leading talents for the digital age.", "Podgotovka vedushchikh kadrov dlya tsifrovoy epokhi.")
    ensure_content("nav.home", "Bosh sahifa", "Home", "Glavnaya")
    ensure_content("nav.about", "Maktab haqida", "About", "O shkole")
    ensure_content("nav.news", "Yangiliklar", "News", "Novosti")
    ensure_content("nav.departments", "Bo'limlar", "Departments", "Otdely")
    ensure_content("nav.contact", "Bog'lanish", "Contact", "Kontakty")
    ensure_content("nav.announcements", "E'lonlar", "Announcements", "Obyavleniya")
    ensure_content("nav.teachers", "Ustozlar", "Teachers", "Uchitelya")
    ensure_content("general.home", "Bosh sahifa", "Home", "Glavnaya")
    ensure_content("general.details", "Batafsil", "Details", "Podrobnee")
    ensure_content("general.read_more", "Batafsil o'qish", "Read more", "Chitat dalej")
    ensure_content("general.detail_page", "Batafsil", "Details", "Podrobnee")
    ensure_content("general.not_available", "Ma'lumot kiritilmagan", "Information not provided", "Informatsiya ne ukazana")
    ensure_content("news.category.all", "Barchasi", "All", "Vse")
    ensure_content("news.category.school", "Maktab yangiliklari", "School news", "Novosti shkoly")
    ensure_content("news.category.announcement", "E'lonlar", "Announcements", "Obyavleniya")
    ensure_content("news.empty.title", "Yangiliklar topilmadi.", "No news found.", "Novosti ne naydeny.")
    ensure_content("news.detail.back", "Barcha yangiliklar", "All news", "Vse novosti")
    ensure_content("news.detail.share", "Ulashish", "Share", "Podelitsya")
    ensure_content("news.detail.copied", "Nusxalandi!", "Copied!", "Skopirovano!")
    ensure_content("departments.category.all", "Barchasi", "All", "Vse")
    ensure_content("departments.category.academic", "Akademik bo'limlar", "Academic departments", "Akademicheskiye otdely")
    ensure_content("departments.category.leadership", "Rahbariyat", "Leadership", "Rukovodstvo")
    ensure_content("departments.category.support", "Qo'llab-quvvatlash", "Support", "Podderzhka")
    ensure_content("departments.category.clubs", "To'garaklar", "Clubs", "Kruzhki")
    ensure_content("departments.empty.title", "Bo'limlar topilmadi.", "No departments found.", "Otdely ne naydeny.")
    ensure_content("departments.card.more", "Batafsil", "Details", "Podrobnee")
    ensure_content("departments.detail.about", "Bo'lim haqida ma'lumot", "About the department", "Otdel haqida ma'lumot")
    ensure_content("departments.detail.subjects", "Maxsus fanlar", "Specialized subjects", "Profilnyye predmety")
    ensure_content("departments.detail.quality.title", "Ta'lim sifati", "Education quality", "Kachestvo obrazovaniya")
    ensure_content("departments.detail.contact.title", "Bog'lanish", "Contact", "Kontakty")
    ensure_content("departments.detail.contact.button", "Savolingiz bormi?", "Have a question?", "Yest vopros?")
    ensure_content("departments.detail.phone.label", "Telefon", "Phone", "Telefon")
    ensure_content("departments.detail.email.label", "Pochta", "Email", "Pochta")
    ensure_content("teachers.category.all", "Barchasi", "All", "Vse")
    ensure_content("teachers.category.leadership", "Rahbariyat", "Leadership", "Rukovodstvo")
    ensure_content("teachers.category.science", "Aniq fanlar", "Sciences", "Tochnyye nauki")
    ensure_content("teachers.category.language", "Tillar", "Languages", "Yazyki")
    ensure_content("teachers.category.natural", "Tabiiy fanlar", "Natural sciences", "Yestestvennyye nauki")
    ensure_content("teachers.header.badge", "Pedagogik jamoa", "Teaching team", "Pedagogicheskiy sostav")
    upsert_content("footer.tagline", "Denov tuman 2-son ixtisoslashtirilgan maktab-internati", "Bright steps to the future. Quality education is the guarantee of a prosperous future.", "Yarkiye shagi v budushcheye. Kachestvennoye obrazovaniye eto garantiya blagopoluchnogo budushchego.")
    upsert_content("footer.desc", "Denov tuman 2-son ixtisoslashtirilgan maktab-internati", "Bright steps to the future.", "Yarkiye shagi v budushcheye.")
    ensure_content("footer.links.title", "Sahifalar", "Pages", "Stranitsy")
    ensure_content("footer.contact.title", "Aloqa", "Contact", "Kontakty")
    ensure_content("footer.map.title", "Xarita", "Map", "Karta")
    ensure_content("footer.rights", "Barcha huquqlar himoyalangan.", "All rights reserved.", "Vse prava zashchishcheny.")
    ensure_content("home.hero.badge", "Rivojlanish va ta'lim markazi", "Center of growth and education", "Tsentr razvitiya i obrazovaniya")
    ensure_content("home.hero.learn_more", "Batafsil ma'lumot", "Learn more", "Uznat bolshe")
    ensure_content("home.hero.teachers_btn", "Ustozlar", "Teachers", "Uchitelya")
    ensure_content("home.stats.teachers", "Malakali ustozlar", "Qualified teachers", "Kvalifitsirovannyye uchitelya")
    ensure_content("home.stats.announcements", "Muhim e'lonlar", "Important announcements", "Vazhnyye obyavleniya")
    ensure_content("home.stats.departments", "Faol bo'limlar", "Active departments", "Aktivnyye otdely")
    ensure_content("home.stats.news", "Yangiliklar", "News", "Novosti")
    ensure_content("home.latest_news.eyebrow", "Media va yangiliklar", "Media and news", "Media i novosti")
    ensure_content("home.latest_news.title", "So'nggi yangiliklar", "Latest news", "Posledniye novosti")
    ensure_content("home.latest_news.all", "Barchasini ko'rish", "View all", "Smotret vse")
    ensure_content("home.latest_news.more", "Batafsil", "Details", "Podrobnee")
    ensure_content("home.announcements.title", "Muhim e'lonlar", "Important announcements", "Vazhnyye obyavleniya")
    ensure_content("home.announcements.subtitle", "O'quvchilar va ota-onalar uchun dolzarb xabarlar", "Current notices for students and parents", "Aktualnyye soobshcheniya dlya uchashchikhsya i roditeley")
    ensure_content("home.announcements.all", "Barcha e'lonlar", "All announcements", "Vse obyavleniya")
    ensure_content("home.announcements.badge", "E'lon", "Announcement", "Obyavleniye")
    ensure_content("home.announcements.more", "Batafsil", "Details", "Podrobnee")
    ensure_content("home.announcements.empty", "Hozircha e'lonlar yo'q.", "No announcements yet.", "Obyavleniy poka net.")
    ensure_content("home.departments.title", "Bo'limlar", "Departments", "Otdely")
    ensure_content("home.departments.subtitle", "Maktabdagi asosiy bo'limlar bilan tanishing", "Explore the main school departments", "Poznakomtes s osnovnymi otdelami shkoly")
    ensure_content("home.departments.all", "Barcha bo'limlar", "All departments", "Vse otdely")
    ensure_content("home.departments.more", "Batafsil", "Details", "Podrobnee")
    ensure_content("home.teachers.cta.title", "Malakali ustozlarimiz bilan tanishing", "Meet our qualified teachers", "Poznakomtes s nashimi kvalifitsirovannymi uchitelyami")
    ensure_content("home.teachers.cta.description", "Har bir fan bo'yicha tajribali pedagoglar o'quvchilarni qo'llab-quvvatlaydi.", "Experienced teachers support students in every subject.", "Opytnyye uchitelya podderzhivayut uchashchikhsya po kazhdomu predmetu.")
    ensure_content("home.teachers.cta.button", "Ustozlar ro'yxati", "Teachers list", "Spisok uchiteley")
    ensure_content("home.contact.cta.title", "Ta'limni biz bilan boshlang", "Start education with us", "Nachnite obrazovaniye s nami")
    ensure_content("home.contact.cta.description", "Dasturlar va imkoniyatlar haqida ko'proq ma'lumot olish uchun bog'laning.", "Contact us to learn more about our programs and opportunities.", "Svazhites s nami, chtoby uznat bolshe o programmakh i vozmozhnostyakh.")
    ensure_content("home.contact.cta.button", "Bog'lanish", "Contact us", "Svazatsya")
    ensure_content("announcements.title", "E'lonlar", "Announcements", "Obyavleniya")
    ensure_content("announcements.subtitle", "Maktabimizning so'nggi e'lon va xabarlari", "Latest announcements and notices from our school", "Posledniye obyavleniya i soobshcheniya nashchey shkoly")
    ensure_content("announcements.badge", "Rasmiy xabarlar", "Official notices", "Ofitsialnyye soobshcheniya")
    ensure_content("announcements.more", "Batafsil o'qish", "Read more", "Chitat dalej")
    ensure_content("announcements.empty.title", "Hozircha e'lonlar yo'q", "No announcements yet", "Obyavleniy poka net")
    ensure_content("announcements.empty.description", "Yangi e'lonlar admin panel orqali qo'shiladi", "New announcements will be added from the admin panel", "Novyye obyavleniya budut dobavleny cherez admin panel")
    ensure_content("teachers.title", "Bizning ustozlar", "Our teachers", "Nashi uchitelya")
    ensure_content("teachers.subtitle", "Malakali va tajribali pedagoglar jamoasi", "A team of qualified and experienced educators", "Komanda kvalifitsirovannykh i opytnykh pedagogov")
    ensure_content("teachers.empty.title", "Hozircha ustozlar qo'shilmagan", "No teachers added yet", "Uchitelya poka ne dobavleny")
    ensure_content("teachers.empty.description", "Admin panel orqali ustozlar ma'lumotini qo'shing", "Add teachers from the admin panel", "Dobavte uchiteley cherez admin panel")
    ensure_content("teachers.card.subject", "Fan", "Subject", "Predmet")
    ensure_content("teachers.card.position", "Lavozim", "Position", "Dolzhnost")
    ensure_content("teachers.card.about", "Ma'lumot", "Information", "Informatsiya")
    ensure_content("teachers.card.achievements", "Yutuqlar", "Achievements", "Dostizheniya")
    ensure_content("teachers.card.about_placeholder", "Ustoz haqida ma'lumot kiritilmagan.", "No teacher information entered.", "Informatsiya ob uchitele ne ukazana.")
    ensure_content("teachers.card.achievements_placeholder", "Yutuqlar kiritilmagan.", "Achievements not entered.", "Dostizheniya ne ukazany.")
    ensure_content("teachers.card.more", "Batafsil", "Details", "Podrobnee")
    ensure_content("teacher.detail.about", "Ustoz haqida", "About the teacher", "Ob uchitele")
    ensure_content("teacher.detail.achievements", "Erishgan yutuqlar", "Achievements", "Dostizheniya")
    ensure_content("teacher.detail.subject", "O'qitadigan fan", "Subject taught", "Prepodavayemyy predmet")
    ensure_content("teacher.detail.position", "Lavozimi", "Position", "Dolzhnost")
    ensure_content("teacher.detail.related", "Boshqa ustozlar", "Other teachers", "Drugiye uchitelya")
    ensure_content("teacher.detail.back", "Ustozlar ro'yxatiga qaytish", "Back to teachers", "Nazad k spisku uchiteley")
    ensure_content("contact.title", "Bog'lanish", "Contact", "Kontakty")
    ensure_content("contact.subtitle", "Biz bilan bog'laning va savollaringizga javob oling.", "Contact us and get answers to your questions.", "Svazhites s nami i poluchite otvety na svoi voprosy.")
    ensure_content("contact.form.title", "Xabar yuborish", "Send a message", "Otpravit soobshcheniye")
    ensure_content("contact.form.subtitle", "Savollaringiz bo'lsa, ushbu shaklni to'ldirib yuboring.", "Fill out the form if you have any questions.", "Zapolnite formu, yesli u vas yest voprosy.")
    upsert_content("contact.form.success.title", "Xabaringiz qabul qilindi!", "Your message has been received!", "Vashe soobshcheniye prinyato!")
    upsert_content("contact.form.success.description", "Xabaringiz qabul qilindi. Sizga email orqali javob beramiz.", "Your message has been received. We will reply by email.", "Vashe soobshcheniye prinyato. My otvetim vam po email.")
    ensure_content("contact.form.full_name", "To'liq ismingiz", "Your full name", "Vashe polnoye imya")
    ensure_content("contact.form.email", "Email manzilingiz", "Your email address", "Vash email")
    ensure_content("contact.form.message", "Xabar matni...", "Message text...", "Tekst soobshcheniya...")
    ensure_content("contact.form.submit", "Xabarni yuborish", "Send message", "Otpravit soobshcheniye")
    ensure_content("contact.card.address.title", "Manzil", "Address", "Adres")
    ensure_content("contact.card.phone.title", "Telefon raqam", "Phone number", "Nomer telefona")
    ensure_content("contact.card.phone.schedule", "Dushanba - Shanba: 08:00 - 18:00", "Monday - Saturday: 08:00 - 18:00", "Ponedelnik - Subbota: 08:00 - 18:00")
    ensure_content("contact.card.email.title", "Elektron pochta", "Email", "Elektronnaya pochta")
    ensure_content("dept.detail.sidebar.quality.percent", "95", "95", "95")
    ensure_content("dept.detail.sidebar.phone.value", "+998-76-228-25-64", "+998-76-228-25-64", "+998-76-228-25-64")
    ensure_content("dept.detail.sidebar.email.value", "info@denov2sonimi.uz", "info@denov2sonimi.uz", "info@denov2sonimi.uz")
    ensure_content("news.detail.contact.address.value", "Denov shahar, Surxandaryo viloyati", "Denov city, Surxandarya region", "Denov, Surxandarya")
    ensure_content("news.detail.contact.phone.value", "+998-76-228-25-64", "+998-76-228-25-64", "+998-76-228-25-64")
    ensure_content("news.detail.contact.email.value", "info@denov2sonimi.uz", "info@denov2sonimi.uz", "info@denov2sonimi.uz")
    ensure_content("contact.card.email.value", "info@denov2sonimi.uz", "info@denov2sonimi.uz", "info@denov2sonimi.uz")

    legacy_category_map = {
        "teachers": "academic",
        "leaders": "leadership",
        "staff": "support",
    }
    legacy_teacher_category_map = {
        "leaders": "leadership",
        "teachers": "science",
        "staff": "natural",
        "primary": "natural",
    }
    legacy_department_map = {
        "Tabiiy Fanlar": {
            "name_uz": "Aniq va tabiiy fanlar bo'limi",
            "description_uz": "Matematika, fizika, biologiya va kimyo fanlari bo'yicha chuqurlashtirilgan ta'lim yo'nalishi.",
            "category_key": "academic",
            "has_subjects": True,
            "subjects_uz": "<ul><li>Matematika</li><li>Fizika</li><li>Biologiya</li><li>Kimyo</li></ul>",
        },
        "Matematika fanlari ustozi": {
            "name_uz": "Aniq va tabiiy fanlar bo'limi",
            "description_uz": "Matematika, fizika, biologiya va kimyo fanlari bo'yicha chuqurlashtirilgan ta'lim yo'nalishi.",
            "category_key": "academic",
            "has_subjects": True,
            "subjects_uz": "<ul><li>Matematika</li><li>Fizika</li><li>Biologiya</li><li>Kimyo</li></ul>",
        },
        "Riyoziyat va Informatika": {
            "name_uz": "Raqamli texnologiyalar bo'limi",
            "description_uz": "Informatika, dasturlash va raqamli ko'nikmalarni rivojlantirishga mas'ul bo'lim.",
            "category_key": "academic",
            "has_subjects": True,
            "subjects_uz": "<ul><li>Informatika</li><li>Dasturlash</li><li>Robototexnika</li></ul>",
        },
        "Ingliz tili fani ustozi": {
            "name_uz": "Xorijiy tillar bo'limi",
            "description_uz": "Ingliz va boshqa xorijiy tillarni zamonaviy metodlar asosida o'qituvchi bo'lim.",
            "category_key": "academic",
            "has_subjects": True,
            "subjects_uz": "<ul><li>Ingliz tili</li><li>Rus tili</li><li>Nemis tili</li></ul>",
        },
        "Til va Literatura": {
            "name_uz": "Ijtimoiy-gumanitar fanlar bo'limi",
            "description_uz": "Ona tili, adabiyot, tarix va huquq yo'nalishlarini qamrab oluvchi bo'lim.",
            "category_key": "support",
            "has_subjects": True,
            "subjects_uz": "<ul><li>Ona tili</li><li>Adabiyot</li><li>Tarix</li><li>Huquq</li></ul>",
        },
        "Ona tili va adabiyot ustozi": {
            "name_uz": "Ijtimoiy-gumanitar fanlar bo'limi",
            "description_uz": "Ona tili, adabiyot, tarix va huquq yo'nalishlarini qamrab oluvchi bo'lim.",
            "category_key": "support",
            "has_subjects": True,
            "subjects_uz": "<ul><li>Ona tili</li><li>Adabiyot</li><li>Tarix</li><li>Huquq</li></ul>",
        },
    }

    departments = db.query(Department).all()
    if not departments:
        db.add_all(
            [
                Department(
                    name_uz="Aniq va tabiiy fanlar bo'limi",
                    description_uz="Matematika, fizika, biologiya va kimyo fanlari bo'yicha chuqurlashtirilgan ta'lim yo'nalishi.",
                    category_key="academic",
                    has_subjects=True,
                    subjects_uz="<ul><li>Matematika</li><li>Fizika</li><li>Biologiya</li><li>Kimyo</li></ul>",
                ),
                Department(
                    name_uz="Xorijiy tillar bo'limi",
                    description_uz="Ingliz va boshqa xorijiy tillarni zamonaviy metodlar asosida o'qituvchi bo'lim.",
                    category_key="academic",
                    has_subjects=True,
                    subjects_uz="<ul><li>Ingliz tili</li><li>Rus tili</li><li>Nemis tili</li></ul>",
                ),
                Department(
                    name_uz="Ijtimoiy-gumanitar fanlar bo'limi",
                    description_uz="Ona tili, adabiyot, tarix va huquq yo'nalishlarini qamrab oluvchi bo'lim.",
                    category_key="support",
                    has_subjects=True,
                    subjects_uz="<ul><li>Ona tili</li><li>Adabiyot</li><li>Tarix</li><li>Huquq</li></ul>",
                ),
            ]
        )
    else:
        for department in departments:
            department.category_key = legacy_category_map.get(department.category_key, department.category_key)
            normalized = legacy_department_map.get(department.name_uz)
            if normalized:
                department.name_uz = normalized["name_uz"]
                department.description_uz = normalized["description_uz"]
                department.category_key = normalized["category_key"]
                department.has_subjects = normalized["has_subjects"]
                department.subjects_uz = normalized["subjects_uz"]

    if db.query(Teacher).count() == 0:
        db.add_all(
            [
                Teacher(
                    first_name="Dilshod",
                    last_name="Karimov",
                    position_uz="Oliy toifali o'qituvchi",
                    subject_uz="Matematika",
                    bio_uz="O'quvchilarni olimpiada va kirish imtihonlariga tayyorlashda katta tajribaga ega pedagog.",
                    achievements_uz="Viloyat matematika olimpiadasi g'oliblarini tayyorlagan.\nSTEM loyihalarida bir nechta muvaffaqiyatli guruhga rahbarlik qilgan.",
                    category_key="science",
                    display_order=2,
                    category_display_order=1,
                ),
                Teacher(
                    first_name="Mohira",
                    last_name="Rasulova",
                    position_uz="Chet tili metodisti",
                    subject_uz="Ingliz tili",
                    bio_uz="Kommunikativ yondashuv asosida dars o'tuvchi, xalqaro sertifikatlarga ega ustoz.",
                    achievements_uz="CEFR bo'yicha yuqori natijaga erishgan o'quvchilarni tayyorlagan.\nMaktab debat klubi murabbiyi.",
                    category_key="language",
                    display_order=3,
                    category_display_order=1,
                ),
                Teacher(
                    first_name="Shahlo",
                    last_name="Nazarova",
                    position_uz="Tabiiy fanlar o'qituvchisi",
                    subject_uz="Biologiya",
                    bio_uz="Biologiya va tabiatshunoslik fanlarini zamonaviy metodlar asosida o'qitadi.",
                    achievements_uz="Fan oyliklari va laboratoriya mashg'ulotlarini samarali tashkil etgan.",
                    category_key="natural",
                    display_order=4,
                    category_display_order=1,
                ),
                Teacher(
                    first_name="Zafar",
                    last_name="Toshpulatov",
                    position_uz="Direktor o'rinbosari",
                    subject_uz="Ta'lim sifati nazorati",
                    bio_uz="Pedagogik jamoani boshqarish va o'quv jarayonini muvofiqlashtirish bilan shug'ullanadi.",
                    achievements_uz="Ta'lim sifatini oshirish bo'yicha bir nechta ichki loyihalarni joriy qilgan.",
                    category_key="leadership",
                    display_order=1,
                    category_display_order=1,
                ),
            ]
        )
    else:
        for teacher in db.query(Teacher).all():
            teacher.category_key = legacy_teacher_category_map.get(teacher.category_key, teacher.category_key or "science")
            if teacher.subject_uz == "Boshlang'ich ta'lim":
                teacher.position_uz = "Tabiiy fanlar o'qituvchisi"
                teacher.subject_uz = "Biologiya"
                teacher.bio_uz = "Biologiya va tabiatshunoslik fanlarini zamonaviy metodlar asosida o'qitadi."
                teacher.achievements_uz = "Fan oyliklari va laboratoriya mashg'ulotlarini samarali tashkil etgan."
            if teacher.category_display_order is None and teacher.display_order is not None:
                teacher.category_display_order = teacher.display_order

    if db.query(News).count() == 0:
        db.add_all(
            [
                News(
                    title_uz="Yangi o'quv yili boshlanadi",
                    content_uz="2024-2025 o'quv yili 1-sentyabrdan boshlanadi. Barcha talabalar va o'qituvchilarni tabriklaymiz!",
                    category_key="school",
                    created_date=datetime.utcnow() - timedelta(days=5),
                ),
                News(
                    title_uz="Olimpiada natijasi e'lon qilindi",
                    content_uz="Maktabimiz o'quvchilarining matematika olimpiadasidagi yutuqlari va taqdirlash marosimi sanasi e'lon qilindi.",
                    category_key="announcement",
                    created_date=datetime.utcnow() - timedelta(days=3),
                ),
            ]
        )
    else:
        for item in db.query(News).filter(News.category_key == "agency").all():
            item.category_key = "announcement"

    db.commit()

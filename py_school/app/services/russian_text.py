from __future__ import annotations

import re


CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LATIN_RE = re.compile(r"[A-Za-z]")
TOKEN_RE = re.compile(r"[A-Za-z]+")

TOKEN_OVERRIDES = {
    "glavnaya": "главная",
    "novosti": "новости",
    "otdely": "отделы",
    "otdel": "отдел",
    "kontakty": "контакты",
    "uchitelya": "учителя",
    "uchiteley": "учителей",
    "uchashchikhsya": "учащихся",
    "obyavleniya": "объявления",
    "obyavleniye": "объявление",
    "obyavleniy": "объявлений",
    "podrobnee": "подробнее",
    "rukovodstvo": "руководство",
    "yazyki": "языки",
    "tochnyye": "точные",
    "yestestvennyye": "естественные",
    "pedagogicheskiy": "педагогический",
    "kvalifitsirovannyye": "квалифицированные",
    "vazhnyye": "важные",
    "aktivnyye": "активные",
    "posledniye": "последние",
    "aktualnyye": "актуальные",
    "opytnyye": "опытные",
    "programmakh": "программах",
    "vozmozhnostyakh": "возможностях",
    "poznakomtes": "познакомьтесь",
    "osnovnymi": "основными",
    "stranitsy": "страницы",
    "karta": "карта",
    "zashchishcheny": "защищены",
    "kachestvo": "качество",
    "obrazovaniya": "образования",
    "obrazovaniye": "образование",
    "budushcheye": "будущее",
    "yarkiye": "яркие",
    "missiya": "миссия",
    "vzglyad": "взгляд",
    "nasha": "наша",
    "nash": "наш",
    "sluzheniye": "служение",
    "obshchestvu": "обществу",
    "cherez": "через",
    "kachestvennoye": "качественное",
    "podgotovka": "подготовка",
    "vedushchikh": "ведущих",
    "kadrov": "кадров",
    "dlya": "для",
    "tsifrovoy": "цифровой",
    "epokhi": "эпохи",
    "informatsiya": "информация",
    "ukazana": "указана",
    "vse": "все",
    "shkoly": "школы",
    "shkoly.": "школы.",
    "podelitsya": "поделиться",
    "skopirovano": "скопировано",
    "akademicheskiye": "академические",
    "podderzhka": "поддержка",
    "kruzhki": "кружки",
    "profilnyye": "профильные",
    "predmety": "предметы",
    "yest": "есть",
    "vopros": "вопрос",
    "telefon": "телефон",
    "pochta": "почта",
    "nauki": "науки",
    "sostav": "состав",
    "shagi": "шаги",
    "eto": "это",
    "garantiya": "гарантия",
    "blagopoluchnogo": "благополучного",
    "tsentr": "центр",
    "razvitiya": "развития",
    "uznat": "узнать",
    "bolshe": "больше",
    "soobshcheniya": "сообщения",
    "soobshcheniye": "сообщение",
    "roditeley": "родителей",
    "smotret": "смотреть",
    "opytnyye": "опытные",
    "uchitelyami": "учителями",
    "po": "по",
    "kazhdomu": "каждому",
    "predmetu": "предмету",
    "spisok": "список",
    "nachnite": "начните",
    "s": "с",
    "nami": "нами",
    "svazhites": "свяжитесь",
    "chtoby": "чтобы",
    "ofitsialnyye": "официальные",
    "nashchey": "нашей",
    "komanda": "команда",
    "pedagogov": "педагогов",
    "dobavleny": "добавлены",
    "predmet": "предмет",
    "dolzhnost": "должность",
    "dostizheniya": "достижения",
    "ob": "об",
    "prepodavayemyy": "преподаваемый",
    "drugiye": "другие",
    "nazad": "назад",
    "k": "к",
    "spisku": "списку",
    "otvety": "ответы",
    "svoi": "свои",
    "voprosy": "вопросы",
    "otpravit": "отправить",
    "prinyato": "принято",
    "my": "мы",
    "otvetim": "ответим",
    "vam": "вам",
    "elektronnaya": "электронная",
    "nomer": "номер",
    "adrs": "адрес",
    "adres": "адрес",
    "ponedelnik": "понедельник",
    "subbota": "суббота",
    "denov": "денов",
    "surxandarya": "сурхандарья",
}

SEQUENCE_MAP = (
    ("shch", "щ"),
    ("yye", "ые"),
    ("iye", "ие"),
    ("iya", "ия"),
    ("iyo", "иё"),
    ("zh", "ж"),
    ("kh", "х"),
    ("ts", "ц"),
    ("ch", "ч"),
    ("sh", "ш"),
    ("yu", "ю"),
    ("ya", "я"),
    ("ye", "е"),
    ("yo", "ё"),
    ("iy", "ий"),
    ("yy", "ы"),
)

CHAR_MAP = {
    "a": "а",
    "b": "б",
    "c": "к",
    "d": "д",
    "e": "е",
    "f": "ф",
    "g": "г",
    "h": "х",
    "i": "и",
    "j": "й",
    "k": "к",
    "l": "л",
    "m": "м",
    "n": "н",
    "o": "о",
    "p": "п",
    "q": "к",
    "r": "р",
    "s": "с",
    "t": "т",
    "u": "у",
    "v": "в",
    "w": "в",
    "x": "кс",
    "y": "ы",
    "z": "з",
}

CODE_TOKENS = {"css", "html", "api", "js", "ui", "id"}


def contains_cyrillic(value: str | None) -> bool:
    return bool(value and CYRILLIC_RE.search(value))


def _apply_case(source: str, target: str) -> str:
    if source.isupper():
        return target.upper()
    if source[:1].isupper() and source[1:].islower():
        return target[:1].upper() + target[1:]
    return target


def _transliterate_token(token: str) -> str:
    if token.isupper() and (len(token) <= 4 or token.lower() in CODE_TOKENS):
        return token

    lowered = token.lower()
    if lowered in CODE_TOKENS:
        return token

    if lowered in TOKEN_OVERRIDES:
        return _apply_case(token, TOKEN_OVERRIDES[lowered])

    index = 0
    result = []
    while index < len(lowered):
        for latin, cyrillic in SEQUENCE_MAP:
            if lowered.startswith(latin, index):
                result.append(cyrillic)
                index += len(latin)
                break
        else:
            result.append(CHAR_MAP.get(lowered[index], lowered[index]))
            index += 1

    return _apply_case(token, "".join(result))


def normalize_russian_text(value: str | None) -> str | None:
    if not value or contains_cyrillic(value) or not LATIN_RE.search(value):
        return value
    return TOKEN_RE.sub(lambda match: _transliterate_token(match.group(0)), value)

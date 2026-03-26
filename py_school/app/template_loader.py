from jinja2 import ChoiceLoader, DictLoader, FileSystemLoader
from starlette.templating import Jinja2Templates

from app.database import TEMPLATES_DIR
from app.templates_bundle import TEMPLATE_BUNDLE


def create_templates() -> Jinja2Templates:
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    templates.env.loader = ChoiceLoader(
        [
            FileSystemLoader(str(TEMPLATES_DIR)),
            DictLoader(TEMPLATE_BUNDLE),
        ]
    )
    return templates

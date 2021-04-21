from pathlib import Path
from jinja2 import FileSystemLoader, Environment


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates/"

LOADER = FileSystemLoader(searchpath=TEMPLATES_DIR)

TEMPLATES_ENV = Environment(loader=LOADER)


class Template:

    def get_template(self, name):
        return TEMPLATES_ENV.get_template(name)

    def render(self, name, context=None):
        if context is None:
            context = {}
        return self.get_template(name).render(context)

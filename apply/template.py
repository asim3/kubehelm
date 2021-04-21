from pathlib import Path
from jinja2 import BaseLoader, FileSystemLoader, Environment


BASE_DIR = Path(__file__).resolve().parent.parent


class Template(BaseLoader):
    path = BASE_DIR / "templates/"

    def __init__(self):
        loader = FileSystemLoader(searchpath=self.path)
        self.environment = Environment(loader=loader)

    def get_template(self, name):
        return self.environment.get_template(name)

    def render(self, name, context=None):
        if context is None:
            context = {}
        return self.get_template(name).render(context)

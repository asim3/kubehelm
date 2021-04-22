from jinja2 import FileSystemLoader, Environment
from conf.settings import BASE_DIR


class Template:
    templates_dir = BASE_DIR / "templates/"
    template_name = None

    def __init__(self):
        loader = FileSystemLoader(searchpath=self.templates_dir)
        self.environment = Environment(loader=loader)

    def get_template_name(self):
        if self.template_name is None:
            raise ValueError(
                "%s requires a definition of 'template_name'." % self.__class__.__name__)
        else:
            return self.template_name

    def get_template(self):
        return self.environment.get_template(self.get_template_name())

    def render(self, context=None):
        if context is None:
            context = {}
        self.rendered_template = self.get_template().render(context)
        return self.rendered_template

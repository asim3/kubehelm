from kubernetes.config import load_kube_config
from kubernetes.client import ApiClient
from kubernetes.client.rest import ApiException, ApiValueError
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError
from jinja2 import FileSystemLoader, Environment
from json import loads as json_loads
from yaml import safe_load_all
from re import search as regular_expression_search

from conf import settings


class Template:
    templates_dir = settings.BASE_DIR / "templates/"
    template_name = None

    def __init__(self, **kwargs):
        loader = FileSystemLoader(searchpath=self.templates_dir)
        self.environment = Environment(loader=loader)
        if kwargs.get('template_name'):
            self.template_name = kwargs.get('template_name')

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


class Context(Template):
    required_context = ["namespace", "app_name"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = kwargs
        self.cleaned_data = {}
        self.full_clean()

    def full_clean(self):
        self._assert_required_values()
        self._clean_values()

    def _assert_required_values(self):
        for key in self.required_context:
            if not self.context.get(key):
                raise ValueError("The value of %s is required" % key)

    def _clean_values(self):
        for key, value in self.context.items():
            self.cleaned_data[key] = value
            if hasattr(self, 'clean_%s' % key):
                value = getattr(self, 'clean_%s' % key)()
                self.cleaned_data[key] = value

    def validate_ingress_name(self, value):
        if not value or regular_expression_search('^[0-9\-]|[^a-z0-9\-]|\-$', value):
            return False
        return True

    def clean_namespace(self):
        value = self.cleaned_data["namespace"]
        if self.validate_ingress_name(value):
            return value
        raise ValueError("Invalid namespace: %s" % value)

    def clean_app_name(self):
        value = self.cleaned_data["app_name"]
        if self.validate_ingress_name(value):
            return value
        raise ValueError("Invalid app_name: %s" % value)


class Manifest(Context):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        load_kube_config()

    def get_manifest(self):
        data = self.render(self.cleaned_data)
        return list(safe_load_all(data))

    def print_manifest(self):
        if settings.DEBUG and self.rendered_template:
            print("-" * 80)
            print(self.rendered_template)
            print("-" * 80)
        else:
            print("rendered_template not available!")

    def apply(self, dry_run=False):
        k8s_client = ApiClient()
        manifest = self.get_manifest()

        failures = []
        for data in manifest:
            try:
                create_from_dict(k8s_client, data, dry_run="All")
            except FailToCreateError as failure:
                failures.extend(failure.api_exceptions)

        if failures:
            if settings.DEBUG:
                self.print_manifest()
                for fail in failures:
                    body = json_loads(fail.body)
                    text = "%s[%s]: %s" % (
                        fail.reason, fail.status, body.get('message'))
                    print(text, "\n")
                print("=" * 80)
            raise FailToCreateError(failures)
        elif not dry_run:
            for data in manifest:
                create_from_dict(k8s_client, data)
        else:
            return "valid"

    def update(self):
        pass

    def delete(self):
        pass

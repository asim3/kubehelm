from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError
from kubernetes.client.api_client import ApiClient
from kubernetes.client.exceptions import ApiException, ApiValueError
from jinja2 import FileSystemLoader, Environment
from json import loads as json_loads
from yaml import safe_load_all
from re import search as regular_expression_search

from .mixin import APIFunctionsMixin
from k8s import settings


class Template:
    templates_dir = settings.BASE_DIR / "k8s/templates/"
    template_name = None

    def __init__(self, **kwargs):
        loader = FileSystemLoader(searchpath=self.templates_dir)
        self.environment = Environment(loader=loader)
        self.template_name = kwargs.get('template_name', self.template_name)

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

    def print_rendered_template(self):
        if settings.DEBUG and self.rendered_template:
            print("-" * 80)
            print(self.rendered_template)
            print("-" * 80)
        else:
            print("rendered_template not available!")


class Context(Template):
    required_context = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = kwargs
        self.cleaned_data = {}
        self.full_clean()

    def full_clean(self):
        self._assert_required_values()
        self._clean_values()

    def _assert_required_values(self):
        if isinstance(self.required_context, (list, tuple)):
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


class Manifest(APIFunctionsMixin, Context):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(**kwargs)

    def get_manifest_as_list(self):
        data = self.render(self.cleaned_data)
        manifest = list(safe_load_all(data))
        return [obj for obj in manifest if obj.get("kind") != "Namespace"]

    def _apply(self, dry_run=False):
        k8s_client = ApiClient()
        manifest = self.get_manifest_as_list()

        failures = []
        for data in manifest:
            try:
                create_from_dict(k8s_client, data, dry_run="All")
            except FailToCreateError as failure:
                failures.extend(failure.api_exceptions)

        if failures:
            if settings.DEBUG:
                self.print_rendered_template()
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

    def apply(self, dry_run=False):
        return self.execute("create", self.get_manifest_as_list(), dry_run=dry_run)

    def update(self, dry_run=False):
        return self.execute("patch", self.get_manifest_as_list(), dry_run=dry_run)

    def delete(self, dry_run=False):
        return self.execute("delete", self.get_manifest_as_list(), dry_run=dry_run)
from json import loads as json_loads
from yaml import safe_load_all
from re import search as regular_expression_search

from k8s.core.scripts import RunScriptMixin
from k8s import settings


class Context:
    required_context = None
    default_context = {
        "namespace": "default",
        "image_tag": "latest",
        "port": 80,
    }

    def __init__(self, **kwargs):
        self.context = kwargs
        self.cleaned_data = self.default_context
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


class Helm(Context, RunScriptMixin):
    script_name = "helm.bash"
    chart_name = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(**kwargs)

    def get_args(self):
        assert self.chart_name
        return [
            self.cleaned_data["app_name"],
            self.cleaned_data["namespace"],
            self.chart_name]

    def as_dict(self, text):
        as_dict = json_loads(text)
        info = as_dict.get('info')
        return {
            'name': as_dict.get('name'),
            'namespace': as_dict.get('namespace'),
            'version': as_dict.get('version'),
            'first_deployed': info.get('first_deployed'),
            'last_deployed': info.get('last_deployed'),
            'description': info.get('description'),
            'status': info.get('status'),
            'deleted': info.get('deleted'),
        }

    def apply(self, **kwargs):
        return self.as_dict(self.execute("install", **kwargs))

    def update(self, **kwargs):
        return self.as_dict(self.execute("update", **kwargs))

    def delete(self, **kwargs):
        return self.execute("delete", **kwargs)

    def execute(self, instruction, **kwargs):
        args = self.get_args()
        if kwargs.get("dry_run", None):
            args.append("--dry-run")
        getattr(self, "pre_%s" % instruction)()
        return self._run_script(instruction, *args)

    def pre_install(self, **kwargs):
        pass

    def pre_update(self, **kwargs):
        pass

    def pre_delete(self, **kwargs):
        pass

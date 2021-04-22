from kubernetes.config import load_kube_config
from kubernetes.client import ApiClient
from kubernetes.client.rest import ApiException, ApiValueError
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError
from json import loads as json_loads
from yaml import safe_load_all

from .template import Template

load_kube_config()


class Context(Template):
    required_context = ["namespace", "app_name"]

    def __init__(self, **kwargs):
        super().__init__()
        self.context = kwargs
        self.cleaned_data = {}
        self.full_clean()

    def full_clean(self):
        self._assert_required_values()
        self._clean_values()

    def _assert_required_values(self):
        for key, value in self.context.items():
            if key in self.required_context:
                if not value:
                    raise ValueError("The value of %s is required" % key)

    def _clean_values(self):
        for key, value in self.context.items():
            self.cleaned_data[key] = value
            if hasattr(self, 'clean_%s' % key):
                value = getattr(self, 'clean_%s' % key)()
                self.cleaned_data[key] = value


class ManifestBase(Context):

    def get_manifest(self):
        data = self.render(self.cleaned_data)
        return list(safe_load_all(data))

    def apply(self):
        k8s_client = ApiClient()
        manifest = self.get_manifest()

        failures = []
        for data in manifest:
            try:
                create_from_dict(k8s_client, data, dry_run="All")
            except FailToCreateError as failure:
                failures.extend(failure.api_exceptions)

        if failures:
            for fail in failures:
                body = json_loads(fail.body)
                text = "%s[%s]: %s" % (
                    fail.reason, fail.status, body.get('message'))
                print(text, "\n")
            print("=" * 80)
            raise FailToCreateError(failures)
        else:
            for data in manifest:
                create_from_dict(k8s_client, data)

    def update(self):
        pass

    def delete(self):
        pass

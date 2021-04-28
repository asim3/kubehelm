from kubernetes import client
from kubernetes.client.exceptions import ApiException, ApiValueError
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError
from json import loads as json_loads
from re import compile

from conf import settings


UPPER_FOLLOWED_BY_LOWER_RE = compile('(.)([A-Z][a-z]+)')
LOWER_OR_NUM_FOLLOWED_BY_UPPER_RE = compile('([a-z0-9])([A-Z])')


class APIFunctionsMixin:
    def execute(self, action, manifest_as_list, dry_run=None, **kwargs):
        failures = []
        for single_dict in manifest_as_list:
            try:
                self.execute_from_single_dict(
                    action, single_dict, dry_run="All", **kwargs)
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
            for single_dict in manifest_as_list:
                self.execute_from_single_dict(action, single_dict, **kwargs)
        else:
            return "valid"

    def execute_from_single_dict(self, action, yaml_object, **kwargs):
        exec_func = self.get_api_function(action, yaml_object, **kwargs)
        return exec_func(**self.get_context_data(action, yaml_object, **kwargs))

    def get_api_function(self, action, yaml_object, **kwargs):
        k8s_api = self.get_k8s_api(yaml_object, **kwargs)
        kind = self.clean_kind_name(yaml_object["kind"])
        if hasattr(k8s_api, "{0}_namespaced_{1}".format(action, kind)):
            return getattr(k8s_api, "{0}_namespaced_{1}".format(action, kind))
        else:
            # kwargs.pop('namespace', None)
            return getattr(k8s_api, "{0}_{1}".format(action, kind))

    def get_k8s_api(self, yaml_object, **kwargs):
        if kwargs.pop('testing', False):
            return getattr(client, self.get_api_function_name(yaml_object))
        return getattr(client, self.get_api_function_name(yaml_object))()

    def get_api_function_name(self, yaml_object):
        group, _, version = yaml_object["apiVersion"].partition("/")
        if version == "":
            version = group
            group = "core"
        # Take care for the case e.g. api_type is "apiextensions.k8s.io"
        # Only replace the last instance
        group = "".join(group.rsplit(".k8s.io", 1))
        # convert group name from DNS subdomain format to
        # python class name convention
        group = "".join(word.capitalize() for word in group.split('.'))
        return "{0}{1}Api".format(group, version.capitalize())

    def clean_kind_name(self, kind):
        # Replace CamelCased action_type into snake_case
        kind = UPPER_FOLLOWED_BY_LOWER_RE.sub(r'\1_\2', kind)
        kind = LOWER_OR_NUM_FOLLOWED_BY_UPPER_RE.sub(r'\1_\2', kind).lower()
        return kind

    def get_context_data(self, action, yaml_object, **kwargs):
        context = {
            "namespace": yaml_object["metadata"]["namespace"],
            ** kwargs
        }

        if action in ("create", "patch"):
            context["body"] = yaml_object

        if action in ("patch", "delete"):
            context["name"] = yaml_object["metadata"]["name"]

        return context

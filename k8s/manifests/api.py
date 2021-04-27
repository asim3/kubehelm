from kubernetes import client
from re import compile


UPPER_FOLLOWED_BY_LOWER_RE = compile('(.)([A-Z][a-z]+)')
LOWER_OR_NUM_FOLLOWED_BY_UPPER_RE = compile('([a-z0-9])([A-Z])')


class APIAttributesMixin:

    def as_api_attributes(self, yaml_objects, action):
        return [self.get_from_single_dict(obj, action) for obj in yaml_objects]

    def get_from_single_dict(self, yaml_object, action):
        k8s_api = getattr(client, self.get_api_function_name(yaml_object))()
        kind = self.clean_kind_name(yaml_object["kind"])
        if hasattr(k8s_api, "{0}_namespaced_{1}".format(action, kind)):
            return getattr(k8s_api, "{0}_namespaced_{1}".format(action, kind))
        else:
            return getattr(k8s_api, "{0}_{1}".format(action, kind))

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


#     # Decide which namespace we are going to put the object in,
#     # if any
#     if "namespace" in yaml_object["metadata"]:
#         namespace = yaml_object["metadata"]["namespace"]
#         kwargs['namespace'] = namespace
#     # resources = getattr(k8s_api, "create_namespaced_{0}".format(kind))(
#         # body=yaml_object, **kwargs)
# else:
#     kwargs.pop('namespace', None)
#     # resources = getattr(k8s_api, "create_{0}".format(kind))(
#     # body=yaml_object, **kwargs)
# # return resources

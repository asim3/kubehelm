from kubernetes.config import load_kube_config
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_deployment_spec import V1DeploymentSpec
from kubernetes.client.exceptions import ApiException, ApiValueError
from json import loads as json_loads

from conf import settings


load_kube_config()


class K8sBase:
    apply_class = None
    object_class = None
    spec_class = None
    namespace = None
    name = None
    component = None
    version = None
    managed_by = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clean_error(self, error):
        body = json_loads(error.body)
        return "%s[%s]: %s" % (error.reason, error.status, body.get('message'))

    def get_labels(self):
        labels = {
            "app.kubernetes.io/name": self.name,
            "app.kubernetes.io/instance": self.name,
            "app.kubernetes.io/part-of": self.name,
        }
        if self.component:
            labels["app.kubernetes.io/component"] = self.component
        if self.version:
            labels["app.kubernetes.io/version"] = self.version
        if self.managed_by:
            labels["app.kubernetes.io/managed-by"] = self.managed_by
        return labels

    def get_metadata(self):
        return V1ObjectMeta(
            namespace=self.namespace,
            name=self.name,
            labels=self.get_labels())

    def get_spec(self):
        if self.spec_class:
            return self.spec_class()

    def get_manifest(self):
        if not self.object_class:
            raise NotImplementedError(
                'subclasses of K8sBase must set object_class attribute')
        return self.object_class(metadata=self.get_metadata(), spec=self.get_spec())

    def apply(self, dry_run=None):
        if not self.apply_class:
            raise NotImplementedError(
                'subclasses of K8sBase must set apply_class attribute')
        try:
            return self.apply_class(self.get_manifest(), dry_run=dry_run)
        except ApiException as err:
            return self.clean_error(err)


class Namespace(K8sBase):
    apply_class = CoreV1Api().create_namespace
    object_class = V1Namespace

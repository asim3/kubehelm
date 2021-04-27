from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.exceptions import ApiException

from .base import ModelBase


class Namespace(ModelBase):
    apply_class = CoreV1Api().create_namespace
    object_class = V1Namespace

    def apply(self, dry_run=None):
        try:
            return self.apply_class(self.get_object(), dry_run=dry_run)
        except ApiException as err:
            return self.clean_error(err)

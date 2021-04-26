from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.models.v1_namespace import V1Namespace

from .base import ModelBase


class Namespace(ModelBase):
    apply_class = CoreV1Api().create_namespace
    object_class = V1Namespace

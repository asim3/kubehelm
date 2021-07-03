from kubernetes.client.api import AppsV1Api, CoreV1Api
from kubernetes.client.models import V1Namespace

from kubehelm.models import K8sBaseModel


class Namespace(K8sBaseModel):
    get_class = CoreV1Api().read_namespace
    list_class = CoreV1Api().list_namespace
    apply_class = CoreV1Api().create_namespace
    object_class = V1Namespace


class Deployment(K8sBaseModel):
    get_class = AppsV1Api().read_namespaced_deployment
    list_class = AppsV1Api().list_namespaced_deployment


class StatefulSet(K8sBaseModel):
    get_class = AppsV1Api().read_namespaced_stateful_set
    list_class = AppsV1Api().list_namespaced_stateful_set


class Pod(K8sBaseModel):
    get_class = CoreV1Api().read_namespaced_pod
    list_class = CoreV1Api().list_namespaced_pod

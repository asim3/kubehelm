from kubernetes.client.api import AppsV1Api, CoreV1Api
from kubernetes.client.exceptions import ApiException
from kubernetes.client.models import V1Namespace

from kubehelm.models.base import ModelBase


class Namespace(ModelBase):
    apply_class = CoreV1Api().create_namespace
    object_class = V1Namespace

    def apply(self, dry_run=None):
        try:
            self.apply_class(self.get_object(), dry_run=dry_run)
        except ApiException as err:
            return self.clean_error(err)


class BaseK8sObject:
    limit = 50
    timeout_seconds = 30
    namespace = None
    object_class = None

    def __init__(self, name, namespace):
        self.name = name
        self.namespace = namespace

    def get(self, **kwargs):
        return self.object_class(
            name=self.name,
            namespace=self.namespace,
            **kwargs)


class ReadDeployment(BaseK8sObject):
    object_class = AppsV1Api().read_namespaced_deployment

    def status(self, **kwargs):
        k8s_object = self.get(**kwargs)
        replicas = k8s_object.status.replicas
        ready_replicas = k8s_object.status.ready_replicas
        return (ready_replicas, replicas)

    def is_ready(self, **kwargs):
        k8s_object = self.get(**kwargs)
        replicas = k8s_object.status.replicas
        ready_replicas = k8s_object.status.ready_replicas
        if ready_replicas == replicas:
            return True
        return False


class ReadPod(BaseK8sObject):
    object_class = CoreV1Api().read_namespaced_pod

    def status(self, **kwargs):
        k8s_object = self.get(**kwargs)
        return k8s_object.status.phase

    def is_ready(self, **kwargs):
        k8s_object = self.get(**kwargs)
        return k8s_object.status.container_statuses[0].ready


class BaseListK8sObjects:
    limit = 50
    timeout_seconds = 30
    namespace = None
    object_class = None

    def __init__(self, namespace):
        self.namespace = namespace

    def get(self, **kwargs):
        return self.object_class(
            namespace=self.namespace,
            limit=self.limit,
            timeout_seconds=self.timeout_seconds,
            **kwargs)

    def get_as_list_filter(self, **kwargs):
        filtered_data = []
        data = self.get(**kwargs)
        items = data.to_dict()
        for obj in items.get('items'):
            filtered_data.append(obj["metadata"]["name"])
        return filtered_data


class ListDeployments(BaseListK8sObjects):
    object_class = AppsV1Api().list_namespaced_deployment


class ListPods(BaseListK8sObjects):
    object_class = CoreV1Api().list_namespaced_pod

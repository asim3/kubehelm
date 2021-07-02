from kubernetes.client.api import AppsV1Api, CoreV1Api
from kubernetes.client.exceptions import ApiException
from kubernetes.client.models import V1Namespace

from kubehelm.models.base import K8sBaseModel


class Namespace(K8sBaseModel):
    read_class = CoreV1Api().read_namespace
    list_class = CoreV1Api().list_namespace
    apply_class = CoreV1Api().create_namespace
    object_class = V1Namespace


class Deployment(K8sBaseModel):
    read_class = AppsV1Api().read_namespaced_deployment
    list_class = AppsV1Api().list_namespaced_deployment

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


class Pod(K8sBaseModel):
    read_class = CoreV1Api().read_namespaced_pod
    list_class = CoreV1Api().list_namespaced_pod

    def status(self, **kwargs):
        k8s_object = self.get(**kwargs)
        return k8s_object.status.phase

    def is_ready(self, **kwargs):
        k8s_object = self.get(**kwargs)
        return k8s_object.status.container_statuses[0].ready

from unittest import TestCase
from kubernetes.client import CoreV1Api, ApiextensionsV1Api, RbacAuthorizationV1Api

from kubehelm.models import K8sExecutor


class TestK8sExecutor(TestCase):
    pod = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "namespace": "testspace",
            "name": "test"
        }
    }
    ext = {
        "apiVersion": "apiextensions.k8s.io/v1",
        "kind": "CustomResourceDefinition",
        "metadata": {
            "name": "test-apiextensions"
        }
    }
    rbac = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {
            "name": "test-rbac"
        }
    }

    def test_pod_apply(self):
        api_func = K8sExecutor().get_api_function("create", self.pod, testing=True)
        expected = getattr(CoreV1Api, "create_namespaced_pod")
        self.assertEqual(api_func, expected)

    def test_pod_update(self):
        api_func = K8sExecutor().get_api_function("patch", self.pod, testing=True)
        expected = getattr(CoreV1Api, "patch_namespaced_pod")
        self.assertEqual(api_func, expected)

    def test_pod_delete(self):
        api_func = K8sExecutor().get_api_function("delete", self.pod, testing=True)
        expected = getattr(CoreV1Api, "delete_namespaced_pod")
        self.assertEqual(api_func, expected)

    # -----------------------

    def test_rbac_apply(self):
        api_func = K8sExecutor().get_api_function(
            "create", self.rbac, testing=True)
        expected = getattr(RbacAuthorizationV1Api,
                           "create_cluster_role_binding")
        self.assertEqual(api_func, expected)

    def test_rbac_update(self):
        api_func = K8sExecutor().get_api_function("patch", self.rbac, testing=True)
        expected = getattr(RbacAuthorizationV1Api,
                           "patch_cluster_role_binding")
        self.assertEqual(api_func, expected)

    def test_rbac_delete(self):
        api_func = K8sExecutor().get_api_function(
            "delete", self.rbac, testing=True)
        expected = getattr(RbacAuthorizationV1Api,
                           "delete_cluster_role_binding")
        self.assertEqual(api_func, expected)

    # -----------------------

    def test_ext_apply(self):
        api_func = K8sExecutor().get_api_function("create", self.ext, testing=True)
        expected = getattr(ApiextensionsV1Api,
                           "create_custom_resource_definition")
        self.assertEqual(api_func, expected)

    def test_ext_update(self):
        api_func = K8sExecutor().get_api_function("patch", self.ext, testing=True)
        expected = getattr(ApiextensionsV1Api,
                           "patch_custom_resource_definition")
        self.assertEqual(api_func, expected)

    def test_ext_delete(self):
        api_func = K8sExecutor().get_api_function("delete", self.ext, testing=True)
        expected = getattr(ApiextensionsV1Api,
                           "delete_custom_resource_definition")
        self.assertEqual(api_func, expected)

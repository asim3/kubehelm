from unittest import TestCase
from kubehelm.objects import Namespace, Deployment, StatefulSet, Pod
from kubehelm.apps import Mariadb

import warnings


class TestObjects(TestCase):

    def setUp(self):
        warnings.filterwarnings(
            'ignore', message='Unverified HTTPS request')

    def test_namespace(self):
        actual = Namespace().list_names()
        expected = ['default', 'ingress-nginx', 'cert-manager',
                    'kube-node-lease', 'kube-public', 'kube-system']
        self.assertCountEqual(actual, expected)

        actual = Namespace(name="e", namespace="i").list()
        self.assertEqual(len(actual.get("results")), 6)

        actual = Namespace(name="default").apply()
        expected = {'code': 409, 'status': 'Failure', 'reason': 'AlreadyExists',
                    'message': 'namespaces "default" already exists', 'namespace': None}
        self.assertDictEqual(actual, expected)

        actual = Namespace(name="test-ns").apply()
        expected = {'name': 'test-ns', 'status': 'Active', 'is_ready': True,
                    'namespace': None, 'code': 200}
        self.assertDictEqual(actual, expected)

        actual = Namespace().list()
        self.assertEqual(len(actual.get("results")), 7)

    def test_pod(self):
        actual = Pod(namespace="default").list_names()
        expected = []
        self.assertEqual(actual, expected)

        actual = Pod(namespace="error").list_names()
        expected = []
        self.assertEqual(actual, expected)

        actual = Pod(namespace="ingress-nginx").list_names()
        expected = 3
        self.assertEqual(len(actual), expected)
        pods_names = actual

        actual = Pod(name=pods_names[0], namespace="error").get()
        self.assertEqual(actual['code'], 404)
        self.assertEqual(actual['status'], 'Failure')
        self.assertEqual(actual['reason'], 'NotFound')

        for pod_name in pods_names:
            actual = Pod(
                name=pod_name, namespace="ingress-nginx").get()
            self.assertEqual(actual['code'], 200)
            self.assertEqual(actual['namespace'], 'ingress-nginx')
            self.assertEqual(actual['name'], pod_name)
            self.assertIn(actual['status'], ['Running', 'Succeeded'])
            self.assertTrue(actual['is_ready'])

    def test_deployment(self):
        actual = Deployment(namespace="default").list_names()
        expected = []
        self.assertEqual(actual, expected)

        actual = Deployment(namespace="error").list_names()
        expected = []
        self.assertEqual(actual, expected)

        actual = Deployment(namespace="ingress-nginx").list_names()
        expected = 1
        self.assertEqual(len(actual), expected)
        pods_names = actual

        actual = Deployment(
            name=pods_names[0], namespace="error").get()
        self.assertEqual(actual['code'], 404)
        self.assertEqual(actual['status'], 'Failure')
        self.assertEqual(actual['reason'], 'NotFound')

        for pod_name in pods_names:
            actual = Deployment(
                name=pod_name, namespace="ingress-nginx").get()
            self.assertEqual(actual['code'], 200)
            self.assertEqual(actual['namespace'], 'ingress-nginx')
            self.assertEqual(actual['name'], pod_name)
            self.assertIn(actual['status'], ['Sustained', "Disordered"])
            self.assertTrue(actual['is_ready'])

    def test_stateful_set(self):
        actual = StatefulSet(namespace="default").list_names()
        expected = []
        self.assertEqual(actual, expected)

        actual = StatefulSet(namespace="error").list_names()
        expected = []
        self.assertEqual(actual, expected)

        Mariadb(namespace="default", name="mariadb").install()

        actual = StatefulSet(namespace="default").list_names()
        expected = ["mariadb"]
        self.assertEqual(actual, expected)

        actual = StatefulSet(name="mariadb-0", namespace="error").get()
        self.assertEqual(actual['code'], 404)
        self.assertEqual(actual['status'], 'Failure')
        self.assertEqual(actual['reason'], 'NotFound')

        self.assertIsNone(StatefulSet(
            name="mariadb", namespace="default").wait())

        actual = StatefulSet(name="mariadb", namespace="default").get()
        self.assertEqual(actual['code'], 200)
        self.assertEqual(actual['namespace'], 'default')
        self.assertEqual(actual['name'], "mariadb")
        self.assertIn(actual['status'], ['Sustained', "Disordered"])
        self.assertTrue(actual['is_ready'])

        actual = Pod(name="mariadb-0", namespace="default").get()
        self.assertEqual(actual['code'], 200)
        self.assertEqual(actual['namespace'], 'default')
        self.assertEqual(actual['name'], "mariadb-0")
        self.assertEqual(actual['status'], "Running")
        self.assertTrue(actual['is_ready'])

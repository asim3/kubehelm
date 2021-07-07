from unittest import TestCase
from kubehelm.objects import Namespace, Deployment, StatefulSet, Pod
from kubehelm.apps import Mariadb

import warnings


class TestObjects(TestCase):
    mariadb_context = {
        "namespace": "test-stateful-set",
        "name": "testing-statefulset-db",
        "root_password": "test@#root",
        "database": "staging_production_database",
        "username": "testing_stateful_set_user",
        "password": "test@#user",
    }

    def setUp(self):
        warnings.filterwarnings(
            'ignore', message='Unverified HTTPS request')

    def test_namespace(self):
        actual = Namespace().list_names()
        self.assertGreaterEqual(len(actual), 5)

        actual = Namespace(name="e", namespace="i").list()
        self.assertGreaterEqual(len(actual.get("results")), 5)

        actual = Namespace(name="default").apply()
        expected = {'code': 409, 'status': 'Failure', 'reason': 'AlreadyExists',
                    'message': 'namespaces "default" already exists', 'namespace': None}
        self.assertDictEqual(actual, expected)

        actual = Namespace(name="test-ns").apply()
        expected = {'name': 'test-ns', 'status': 'Active', 'is_ready': True,
                    'namespace': None, 'code': 200}
        self.assertDictEqual(actual, expected)

        actual = Namespace().list()
        self.assertGreaterEqual(len(actual.get("results")), 7)

    def test_pod(self):
        actual = Namespace(name="test-pod").apply()
        expected = {'name': 'test-pod', 'status': 'Active', 'is_ready': True,
                    'namespace': None, 'code': 200}
        self.assertDictEqual(actual, expected)

        actual = Pod(namespace="test-pod").list_names()
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
            self.assertIn(actual['status'], ["Running", "Completed"])
            self.assertTrue(actual['is_ready'])

    def test_deployment(self):
        actual = Namespace(name="test-deploy").apply()
        expected = {'name': 'test-deploy', 'status': 'Active', 'is_ready': True,
                    'namespace': None, 'code': 200}
        self.assertDictEqual(actual, expected)

        actual = Deployment(namespace="test-deploy").list_names()
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
        actual = Namespace(name="test-stateful-set").apply()
        expected = {'name': 'test-stateful-set', 'status': 'Active', 'is_ready': True,
                    'namespace': None, 'code': 200}
        self.assertDictEqual(actual, expected)

        actual = StatefulSet(namespace="test-stateful-set").list_names()
        expected = []
        self.assertEqual(actual, expected)

        actual = StatefulSet(namespace="error").list_names()
        expected = []
        self.assertEqual(actual, expected)

        Mariadb(**self.mariadb_context).install()

        actual = StatefulSet(namespace="test-stateful-set").list_names()
        expected = ["testing-statefulset-db-mariadb"]
        self.assertEqual(actual, expected)

        actual = StatefulSet(name="mariadb-0", namespace="error").get()
        self.assertEqual(actual['code'], 404)
        self.assertEqual(actual['status'], 'Failure')
        self.assertEqual(actual['reason'], 'NotFound')

        self.assertIsNone(StatefulSet(
            name="testing-statefulset-db-mariadb", namespace="test-stateful-set").wait())

        actual = StatefulSet(
            name="testing-statefulset-db-mariadb", namespace="test-stateful-set").get()
        self.assertEqual(actual['code'], 200)
        self.assertEqual(actual['namespace'], 'test-stateful-set')
        self.assertEqual(actual['name'], "testing-statefulset-db-mariadb")
        self.assertIn(actual['status'], ['Sustained', "Disordered"])
        self.assertTrue(actual['is_ready'])

        actual = Pod(name="testing-statefulset-db-mariadb-0",
                     namespace="test-stateful-set").get()
        self.assertEqual(actual['code'], 200)
        self.assertEqual(actual['namespace'], 'test-stateful-set')
        self.assertEqual(actual['name'], "testing-statefulset-db-mariadb-0")
        self.assertEqual(actual['status'], "Running")
        self.assertTrue(actual['is_ready'])

from unittest import TestCase
from kubehelm.objects import Namespace, Deployment, Pod

import warnings


class TestObjects(TestCase):

    def setUp(self):
        warnings.filterwarnings(
            'ignore', message='Unverified HTTPS request')

    def test_namespace(self):
        actual = Namespace().list_names()
        expected = ['default', 'ingress-nginx',
                    'kube-node-lease', 'kube-public', 'kube-system']
        self.assertEqual(actual, expected)

        actual = Namespace(name="e", namespace="i").list()
        self.assertEqual(len(actual.get("results")), 5)

        actual = Namespace(name="default").apply()
        expected = {'code': 409, 'status': 'Failure', 'reason': 'AlreadyExists',
                    'message': 'namespaces "default" already exists', 'namespace': None}
        self.assertEqual(actual, expected)

        actual = Namespace(name="test-ns").apply()
        expected = {'name': 'test-ns', 'status': 'Active',
                    'namespace': None, 'code': 200}
        self.assertEqual(actual, expected)

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

    def test_pod(self):
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

    def test_is_ready(self):
        pass

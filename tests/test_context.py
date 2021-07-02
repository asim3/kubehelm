from unittest import TestCase

from kubehelm.context import Context
from kubehelm.apps import Whoami, Django


class RequiredContext(Context):
    required_context = ["namespace", "app_name"]


class TestContext(TestCase):
    context_error = {
        "value_1": "t1",
        "value_2": "test",
    }
    context = {
        "template_name": "tests/test.yaml",
        "namespace": "ingress-name",
        "app_name": "test",
    }
    invalid_names = [
        "-ingress",
        "ingress-",
        "0ingress",
        "ingress_name",
        "ingress name",
        "الاسم",
    ]
    django_default_context = {
        "manifest_name": "Django",
        "namespace": "default",
        "app_name": "default-django",
        "image_name": "asim3/abcdef",
        "image_tag": "latest",
        "memory_limit": "111Mi",
        "cpu_limit": "333m",
        "secrets": [],
    }
    whoami_default_context = {
        "manifest_name": "Whoami",
        "namespace": "default",
        "app_name": "default-whoami",
        "image_name": "containous/whoami-default",
        "image_tag": "latest",
        "memory_limit": "222Mi",
        "cpu_limit": "444m",
        "secrets": [],
    }
    new_default_context = {
        'manifest_name': 'Whoami',
        'namespace': 'default',
        'app_name': 'default-new',
        'image_name': 'containous/whoami',
        'image_tag': 'latest',
        'memory_limit': '128Mi',
        'cpu_limit': '50m',
        'secrets': [],
    }

    def assert_ingress_name(self, **kwargs):
        key, value = list(kwargs.items())[0]
        expected = "Invalid %s: %s" % (key, value)
        with self.assertRaises(ValueError) as err:
            context = self.context.copy()
            context[key] = value
            RequiredContext(**context)
        self.assertEqual(str(err.exception), expected)

    def test_assert_required_namespace(self):
        expected = "The value of namespace is required"
        with self.assertRaises(ValueError) as exception_context:
            RequiredContext(**self.context_error)
        self.assertEqual(str(exception_context.exception), expected)

    def test_assert_required_app_name(self):
        expected = "The value of app_name is required"
        with self.assertRaises(ValueError) as exception_context:
            RequiredContext(namespace="test-app-name")
        self.assertEqual(str(exception_context.exception), expected)

    def test_validate_ingress_name(self):
        for name in self.invalid_names:
            self.assert_ingress_name(namespace=name)
            self.assert_ingress_name(app_name=name)

    def test_default_context(self):
        whoami_context = Whoami(**self.whoami_default_context).cleaned_data
        self.assertDictEqual(self.whoami_default_context, whoami_context)

        django_context = Django(**self.django_default_context).cleaned_data
        self.assertDictEqual(self.django_default_context, django_context)

        new_context = Whoami(**self.new_default_context).cleaned_data
        self.assertDictEqual(self.new_default_context, new_context)

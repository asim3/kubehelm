from unittest import TestCase
from manifests.manifest import Context


class TestContext(TestCase):
    context_error = {
        "value_1": "t1",
        "value_2": "test",
    }
    context = {
        "template_name": "test.yaml",
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

    def assert_ingress_name(self, **kwargs):
        key, value = list(kwargs.items())[0]
        expected = "Invalid %s: %s" % (key, value)
        with self.assertRaises(ValueError) as err:
            context = self.context.copy()
            context[key] = value
            Context(**context)
        self.assertEqual(str(err.exception), expected)

    def test_context(self):
        actual = Context(**self.context).render()
        expected = "apiVersion: \nmetadata:\n  name: \n  labels:\n    label: test"
        self.assertEqual(actual, expected)

    def test_assert_required_namespace(self):
        expected = "The value of namespace is required"
        with self.assertRaises(ValueError) as exception_context:
            Context(**self.context_error)
        self.assertEqual(str(exception_context.exception), expected)

    def test_assert_required_app_name(self):
        expected = "The value of app_name is required"
        with self.assertRaises(ValueError) as exception_context:
            Context(namespace="test-app-name")
        self.assertEqual(str(exception_context.exception), expected)

    def test_validate_ingress_name(self):
        for name in self.invalid_names:
            self.assert_ingress_name(namespace=name)
            self.assert_ingress_name(app_name=name)

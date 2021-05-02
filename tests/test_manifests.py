from unittest import TestCase
from k8s.models.manifest import Manifest


class RequiredManifest(Manifest):
    required_context = ["namespace", "app_name"]


class TestManifestTemplate(TestCase):
    context = {
        "template_name": "tests/test.yaml",
        "namespace": "testspace",
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
            RequiredManifest(**context)
        self.assertEqual(str(err.exception), expected)

    def test_validate_ingress_name(self):
        for name in self.invalid_names:
            self.assert_ingress_name(namespace=name)
            self.assert_ingress_name(app_name=name)

    def test_assert_required_namespace(self):
        expected = "The value of namespace is required"
        with self.assertRaises(ValueError) as exception_context:
            RequiredManifest()
        self.assertEqual(str(exception_context.exception), expected)

        with self.assertRaises(ValueError) as exception_context:
            RequiredManifest(value_1="t1", value_2="test")
        self.assertEqual(str(exception_context.exception), expected)

    def test_assert_required_app_name(self):
        expected = "The value of app_name is required"
        with self.assertRaises(ValueError) as exception_context:
            RequiredManifest(namespace="test-app-name")
        self.assertEqual(str(exception_context.exception), expected)

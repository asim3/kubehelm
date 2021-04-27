from unittest import TestCase
from k8s.manifests.base import Template


class TestTemplate(TestCase):
    context = {
        "value_1": "t1",
        "value_2": "test",
    }

    def setUp(self):
        self.template = Template(template_name="tests/test.yaml")

    def test_render(self):
        actual = self.template.render(self.context)
        expected = "apiVersion: t1\nmetadata:\n  name: test\n  labels:\n    label: test"
        self.assertEqual(actual, expected)

    def test_assert_required_values(self):
        expected = "Template requires a definition of 'template_name'."
        with self.assertRaises(ValueError) as exception_context:
            Template().render(self.context)
        self.assertEqual(str(exception_context.exception), expected)

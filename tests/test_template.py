from unittest import TestCase
from manifests.manifest import Template


class TestTemplate(TestCase):
    context = {
        "value_1": "t1",
        "value_2": "test",
    }

    def setUp(self):
        self.template = Template(template_name="test.yaml")

    def test_render(self):
        actual = self.template.render(self.context)
        expected = "apiVersion: t1\nmetadata:\n  name: test\n  labels:\n    label: test"
        self.assertEqual(actual, expected)

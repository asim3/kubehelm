from unittest import TestCase
from manifests.manifest import Manifest


# class TestTemplate(TestCase):
#     context = {
#         "value_1": "t1",
#         "value_2": "test",
#     }

#     def setUp(self):
#         self.template = Manifest(template_name="test.yaml")

#     def test_render(self):
#         actual = self.template.render(self.context)
#         expected = "apiVersion: t1\nmetadata:\n  name: test\n  labels:\n    label: test"
#         self.assertEqual(actual, expected)

#     def test_exception(self):
#         with self.assertRaises(ValueError) as exception_context:
#             raise ValueError("my text")
#         self.assertEqual(str(exception_context.exception), "my text")

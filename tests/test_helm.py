from unittest import TestCase

from k8s.models.apps import Wordpress
from k8s.models.scripts import RunScriptError


class TestHelm(TestCase):
    context = {
        "namespace": "default",
        "app_name": "helm-test",
    }

    def tearDown(self):
        try:
            Wordpress(**self.context).delete()
        except RunScriptError:
            pass

    def test_install_upgrade_uninstall(self):
        results = Wordpress(**self.context).install()
        self.assertEqual(results.get("description"), "Install complete")
        results = Wordpress(**self.context).update()
        self.assertEqual(results.get("description"), "Upgrade complete")
        results = Wordpress(**self.context).delete()
        self.assertEqual(results.strip(), "release \"helm-test\" uninstalled")

    def test_assert_required_app_name(self):
        expected = "The value of app_name is required"
        with self.assertRaises(ValueError) as exception_context:
            Wordpress(namespace="test-app-name").install(dry_run=True)
        self.assertEqual(str(exception_context.exception).strip(), expected)

    def test_release_not_found(self):
        expected = "Error: UPGRADE FAILED: \"test\" has no deployed releases"
        with self.assertRaises(RunScriptError) as exception_context:
            kwargs = {"namespace": "test-app-name", "app_name": "test"}
            Wordpress(**kwargs).update(dry_run=True)
        self.assertEqual(str(exception_context.exception).strip(), expected)

from unittest import TestCase
from k8s.apps import Whoami, Django, Mariadb, Wordpress


class TestApps(TestCase):
    context = {
        "namespace": "default",
        "app_name": "my-app",
    }

    def test_apply_whoami(self):
        manifest = Whoami(**self.context).apply(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_apply_django(self):
        manifest = Django(**self.context).apply(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_apply_mariadb(self):
        manifest = Mariadb(**self.context).apply(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_apply_wordpress(self):
        manifest = Wordpress(**self.context).apply(dry_run=True)
        self.assertEqual(manifest.get("description"), "Dry run complete")

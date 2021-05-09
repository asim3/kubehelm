from unittest import TestCase
from k8s.apps import Whoami, Django, Mariadb, Wordpress


class TestApps(TestCase):
    context = {
        "namespace": "default",
        "app_name": "my-app",
    }

    def test_install_whoami(self):
        manifest = Whoami(**self.context).install(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_install_django(self):
        manifest = Django(**self.context).install(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_install_mariadb(self):
        manifest = Mariadb(**self.context).install(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_install_wordpress(self):
        manifest = Wordpress(**self.context).install(dry_run=True)
        self.assertEqual(manifest.get("description"), "Dry run complete")

from unittest import TestCase
from kubehelm.apps import Whoami, Django, Mariadb, Wordpress


class TestApps(TestCase):
    context = {
        "namespace": "default",
        "name": "my-app",
        "image_name": "asim3/django",
        "image_tag": "latest",
    }
    mariadb_context = {
        "namespace": "default",
        "name": "testing-db",
        "root_password": "test@#root",
        "database": "staging_production_database",
        "username": "testing_user",
        "password": "test@#user",
    }

    def test_install_whoami(self):
        manifest = Whoami(**self.context).install(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_install_django(self):
        manifest = Django(**self.context).install(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_install_mariadb(self):
        manifest = Mariadb(**self.mariadb_context).install(dry_run=True)
        self.assertEqual(manifest.get("description"), "Dry run complete")

    def test_install_wordpress(self):
        manifest = Wordpress(**self.context).install(dry_run=True)
        self.assertEqual(manifest.get("description"), "Dry run complete")

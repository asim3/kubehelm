from unittest import TestCase
from manifests.apps import Whoami


class TestApps(TestCase):
    context = {
        "namespace": "default",
        "app_name": "whoami",
    }

    def test_whoami(self):
        manifest = Whoami(**self.context).apply(dry_run=True)
        self.assertEqual(manifest, "valid")

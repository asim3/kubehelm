from unittest import TestCase
from k8s.manifests.apps import Whoami, Manifests


class TestApps(TestCase):
    context = {
        "namespace": "default",
        "app_name": "whoami",
    }

    def test_apply_whoami(self):
        manifest = Whoami(**self.context).apply(dry_run=True)
        self.assertEqual(manifest, "valid")

    def test_whoami(self):
        manifest = getattr(Manifests, "whoami")
        self.assertEqual(manifest, Whoami)

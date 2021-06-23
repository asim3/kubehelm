from unittest import TestCase
from json import loads as json_loads
from time import sleep

from kubehelm.apps import Ingress, Cert, Issuerstaging


class TestIngress(TestCase):
    def test_install_upgrade(self):
        results = Ingress().install()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Install complete")

        results = Ingress().update()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Upgrade complete")


class TestCert(TestCase):
    def test_install_upgrade(self):
        results = Cert().install()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Install complete")

        results = Cert().update()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Upgrade complete")

        sleep(60)

        # Issuerstaging
        results = Issuerstaging().install()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Install complete")

        results = Issuerstaging().update()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Upgrade complete")

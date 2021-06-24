from unittest import TestCase
from json import loads as json_loads
from time import sleep
from subprocess import run, DEVNULL

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

        for _ in range(50):
            sleep(1)
            shell = run(["kubectl", "get", "ValidatingWebhookConfiguration/cert-manager-webhook"],
                        shell=True, stdout=DEVNULL, stderr=DEVNULL)
            if shell.returncode == 0:
                break

        # Issuer
        results = Issuerstaging().install()
        server = json_loads(results).get("spec").get("acme").get("server")
        email = json_loads(results).get("spec").get("acme").get("email")
        self.assertEqual(email, "asim@asim.com")
        self.assertEqual(
            server, "https://acme-staging-v02.api.letsencrypt.org/directory")

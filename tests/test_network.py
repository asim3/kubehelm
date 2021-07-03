from unittest import TestCase
from json import loads as json_loads
from time import sleep
from subprocess import run, PIPE, DEVNULL

from kubehelm.objects import Deployment, Pod
from kubehelm import apps

import requests
import warnings


class TestAppsNetwork(TestCase):
    apps_contexts = [
        {
            "namespace": "default",
            "manifest_name": "Whoami",
            "name": "whoami-test1",
        },
        # {
        #     "namespace": "default",
        #     "manifest_name": "Django",
        #     "name": "django-test2",
        #     "image_name": "asim3/django",
        #     "image_tag": "latest",
        # },
        {
            "namespace": "default",
            "manifest_name": "Whoami",
            "name": "whoami-test3",
        },
    ]

    def setUp(self):
        warnings.filterwarnings(
            'ignore', message='Unverified HTTPS request')

    def test_manifests_apps_networks(self):
        for app_context in self.apps_contexts:
            self.assert_network_ok(app_context)

    # def test_mariadb_networks(self):
    #     self.assert_network_ok({
    #         "namespace": "default",
    #         "manifest_name": "Mariadb",
    #         "name": "mariadb-test4",
    #     })

    def assert_network_ok(self, app_context):
        url = 'https://%s.kube-helm.local/api' % app_context.get("name")
        app = getattr(apps, app_context.get("manifest_name"))(**app_context)
        app.install()
        Pod(name=app_context.get("name"),
            namespace=app_context.get("namespace")).wait()
        results = self.get_url_results(url)
        app.delete()
        headers = results.get("headers")
        self.assertEqual(headers.get("X-Forwarded-Port"), ['443'])
        self.assertEqual(headers.get("X-Forwarded-Proto"), ['https'])
        self.assertEqual(headers.get("X-Scheme"), ['https'])
        self.assertEqual(results.get("method"), "GET")
        self.assertEqual(results.get("hostname"), app_context.get("name"))

    def get_url_results(self, url):
        for _ in range(64):
            sleep(1)
            results = requests.get(url, verify=False)
            if results.ok and results.status_code == 200:
                return results.json()
        return 0


class TestCert(TestCase):
    def test_install_cert(self):
        results = apps.Cert().install()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Install complete")

        results = apps.Cert().update()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Upgrade complete")
        self.assertIsNone(Deployment(name='cert-manager-webhook',
                                     namespace='cert-manager').wait())
        self.assertTrue(Deployment(name='cert-manager-webhook',
                                   namespace='cert-manager').is_ready())

    def test_letsencrypt_issuer(self):
        sleep(10)
        print("=="*88)
        results = apps.Issuerstaging().install()
        server = json_loads(results).get("spec").get("acme").get("server")
        email = json_loads(results).get("spec").get("acme").get("email")
        self.assertEqual(email, "asim@asim.com")
        self.assertEqual(
            server, "https://acme-staging-v02.api.letsencrypt.org/directory")
        print("test_letsencrypt_issuer")


# class TestIngress(TestCase):
#     def test_install_upgrade(self):
#         results = apps.Ingress().install()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Install complete")

#         results = apps.Ingress().update()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Upgrade complete")

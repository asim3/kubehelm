from unittest import TestCase
from json import loads as json_loads
from time import sleep
from subprocess import run, PIPE, DEVNULL

from kubehelm.objects import ReadDeployment, ReadPod
from kubehelm import apps

import requests
import warnings


class TestAppsNetwork(TestCase):
    apps_contexts = [
        {
            "namespace": "default",
            "app_name": "whoami",
        },
        {
            "namespace": "default",
            "app_name": "django",
            "image_name": "asim3/django",
            "image_tag": "latest",
        },
        {
            "namespace": "default",
            "app_name": "whoami",
        },
    ]

    def setUp(self):
        warnings.filterwarnings(
            'ignore', message='Unverified HTTPS request')

    def test_manifests_apps_networks(self):
        for app_context in self.apps_contexts:
            name = app_context.get("app_name")
            shell_script = "kubectl get pod/%s -o jsonpath='{.status.containerStatuses[].ready}'" % name
            self.assert_network_ok(
                name, app_context, shell_script)

    # def test_mariadb_networks(self):
    #     shell_script = "kubectl get statefulset/mariadb -o jsonpath='{.status.readyReplicas}'"
    #     self.assert_network_ok("mariadb", shell_script)

    def assert_network_ok(self, name, app_context, shell_script):
        url = 'https://%s.kube-helm.local' % name
        app_class = getattr(apps, name.capitalize())(**app_context)
        app_class.install()
        self.assert_kubectl_ready_status(shell_script)
        status_code = self.get_url_status_code(url)
        app_class.delete()
        self.assertEqual(status_code, 200)

    def assert_kubectl_ready_status(self, app_context):
        for _ in range(500):
            sleep(5)
            name = app_context.get("name")
            namespace = app_context.get("namespace")
            pod = ReadPod(name, namespace).get()
            for conditions in pod.status.conditions:
                if conditions.type == "Ready":
                    break

    def get_url_status_code(self, url):
        for _ in range(30):
            sleep(3)
            results = requests.get(url, verify=False)
            if results.ok:
                return results.status_code
        return 0


class TestCert(TestCase):
    def test_install_cert(self):
        results = apps.Cert().install()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Install complete")

        results = apps.Cert().update()
        description = json_loads(results).get("info").get("description")
        self.assertEqual(description, "Upgrade complete")
        self.wait_for_cert_webhook()
        self.install_and_test_letsencrypt_issuer()

    def wait_for_cert_webhook(self):
        for _ in range(500):
            sleep(1)
            deployment = ReadDeployment(
                'cert-manager-webhook', 'cert-manager').get()
            ready_replicas = deployment.status.ready_replicas
            if ready_replicas == "1":
                break

    def install_and_test_letsencrypt_issuer(self):
        sleep(10)
        results = apps.Issuerstaging().install()
        server = json_loads(results).get("spec").get("acme").get("server")
        email = json_loads(results).get("spec").get("acme").get("email")
        self.assertEqual(email, "asim@asim.com")
        self.assertEqual(
            server, "https://acme-staging-v02.api.letsencrypt.org/directory")


# class TestIngress(TestCase):
#     def test_install_upgrade(self):
#         results = apps.Ingress().install()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Install complete")

#         results = apps.Ingress().update()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Upgrade complete")

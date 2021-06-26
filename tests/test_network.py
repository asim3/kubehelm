from unittest import TestCase
from json import loads as json_loads
from time import sleep
from subprocess import run, PIPE, DEVNULL

from kubehelm import apps

import requests


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
            shell = run(["kubectl get -n cert-manager deployment/cert-manager-webhook -o jsonpath='{.status.readyReplicas}'"],
                        shell=True, stdout=PIPE, stderr=DEVNULL)
            if shell.stdout.decode() == "1":
                break

    def install_and_test_letsencrypt_issuer(self):
        sleep(10)
        results = apps.Issuerstaging().install()
        server = json_loads(results).get("spec").get("acme").get("server")
        email = json_loads(results).get("spec").get("acme").get("email")
        self.assertEqual(email, "asim@asim.com")
        self.assertEqual(
            server, "https://acme-staging-v02.api.letsencrypt.org/directory")


class TestNetwork(TestCase):
    manifests_apps_list = [
        "whoami",
        "django",
    ]
    helm_apps_list = [
        "mariadb",
        "phpmyadmin",
        "wordpress",
        "osclass",
    ]

    def test_manifests_apps_networks(self):
        shell_status = "true"
        for name in self.manifests_apps_list:
            shell_script = "kubectl get pod/%s -o jsonpath='{.status.containerStatuses[].ready}'" % name
            self.assert_network_ok(name, shell_script, shell_status)

    # def test_mariadb_networks(self):
    #     shell_status = "1"
    #     shell_script = "kubectl get statefulset/mariadb -o jsonpath='{.status.readyReplicas}'"
    #     self.assert_network_ok("mariadb", shell_script, shell_status)

    def assert_network_ok(self, name, shell_script, shell_status):
        url = 'https://%s.kube-helm.local' % name
        app_context = {"namespace": "default", "app_name": name}
        if name == "django":
            app_context.update(image_name="asim3/django", image_tag="latest")
        app_class = getattr(apps, name.capitalize())(**app_context)
        app_class.install()
        self.assert_kubectl_ready_status(name, shell_script, shell_status)
        status_code = self.get_url_status_code(url)
        app_class.delete()
        self.assertEqual(status_code, 200)

    def assert_kubectl_ready_status(self, shell_script, shell_status):
        for _ in range(500):
            sleep(5)
            status = run([shell_script], shell=True,
                         stdout=PIPE, stderr=DEVNULL)
            if status.stdout.decode() == shell_status:
                break

    def get_url_status_code(self, url):
        for _ in range(50):
            sleep(5)
            results = requests.get(url, verify=False)
            status_code = results.status_code

            print(_, url, "status_code:", status_code)

            run(['echo ; echo "==="; curl -k %s || echo 5678' % url], shell=True)
            if results.ok:
                return results.status_code
        run(["kubectl get all,ing,ep"], shell=True)
        return 0


# class TestIngress(TestCase):
#     def test_install_upgrade(self):
#         results = apps.Ingress().install()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Install complete")

#         results = apps.Ingress().update()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Upgrade complete")

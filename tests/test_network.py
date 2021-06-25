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
            # TODO: delete this
            print(_, "cert-manager-webhook status:", shell.stdout.decode())
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
        print("email-"*88)
        print(email)
        print("email-"*88)


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

    def test_mariadb_networks(self):
        shell_status = "true"
        shell_script = "kubectl get statefulset/mariadb -o jsonpath='{.status.readyReplicas}'"
        self.assert_network_ok("mariadb", shell_script, shell_status)

    def assert_network_ok(self, name, shell_script, shell_status):
        status_code = 0
        app_context = {"namespace": "default", "app_name": "test-%s" % name}

        if name == "django":
            app_context.update(image_name="asim3/django", image_tag="latest")

        app_class = getattr(apps, name.capitalize())(**app_context)
        app_class.install()

        for _ in range(500):
            sleep(5)
            status = run([shell_script], shell=True,
                         stdout=PIPE, stderr=DEVNULL)
            if status.stdout.decode() == shell_status:
                break
            print(_, name, "ready status:", status.stdout.decode())

        run(["cat /etc/hosts"], shell=True)

        for _ in range(50):
            sleep(5)
            results = requests.get(
                'http://%s.kube-helm.local' % name, verify=False)
            status_code = results.status_code
            print(_, 'http://%s.kube-helm.local' %
                  name, "status_code:", status_code)
            if results.ok:
                break

        app_class.delete()

        if status_code != 200:
            print()
        self.assertEqual(status_code, 200)


# class TestIngress(TestCase):
#     def test_install_upgrade(self):
#         results = apps.Ingress().install()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Install complete")

#         results = apps.Ingress().update()
#         description = json_loads(results).get("info").get("description")
#         self.assertEqual(description, "Upgrade complete")

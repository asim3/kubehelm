from unittest import TestLoader, TextTestRunner
from subprocess import run, PIPE
from sys import exit
# from argparse import ArgumentParser
from k8s import apps
from k8s.models.manifest import Manifest
from k8s.models.objects import Namespace, ListK8sObjects
from k8s import settings


class Controller:
    def __init__(self, *args):
        command = ""
        for i, arg in enumerate(args[1:], 2):
            command = arg if not command else "%s_%s" % (command, arg)
            method = getattr(self, command, None)
            if method:
                return method(*args[i:])
        self._print_help()

    def _print_help(self):
        for method in self.__dir__():
            if not method.startswith('_'):
                print(method.replace('_', ' '))

    def _run_script(self, path, *args):
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE)
        return sub_pro.stdout.decode()

    def _get_manifest(self, *args):
        try:
            name = args[0]
            return getattr(apps, name.capitalize())
        except (IndexError, AttributeError) as err:
            manifests_list = "\n  ".join(self._get_all_manifests())
            print("manifests are: \n  %s" % manifests_list)
            print("="*80)
            raise err

    def _get_all_manifests(self):
        return [method for method in dir(apps) if not method.startswith('_')]

    def test(self, *args):
        loader = TestLoader().discover(settings.BASE_DIR / "tests")
        TextTestRunner().run(loader)

    def apply(self, *args):
        manifest = self._get_manifest(*args)
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        if namespace != "default":
            Namespace(name=namespace).apply(sleep=True)
        manifest(namespace=namespace, app_name=app_name).apply()

    def list(self, *args):
        print(ListK8sObjects(args[0]).deployments())
        print("="*99)
        print(ListK8sObjects(args[0]).pods())

    def update(self, *args):
        manifest = self._get_manifest(*args)
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        manifest(namespace=namespace, app_name=app_name).update()

    def delete(self, *args):
        manifest = self._get_manifest(*args)
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        manifest(namespace=namespace, app_name=app_name).delete()

    def update_ingress(self, *args):
        path = settings.BASE_DIR / "scripts/update_ingress.bash"
        print(self._run_script(path, *args))

    def update_cert(self, *args):
        "update certificate manager"
        path = settings.BASE_DIR / "scripts/update_certificate_manager.bash"
        print(self._run_script(path, *args))

    def setup_ingress(self, provider=None):
        providers = ("do", "aws", "cloud", "kind", "scw", "baremetal")
        if not provider:
            print("providers:", *providers)
            provider = input("provider name: ")
        if not str(provider) in providers:
            raise ValueError("provider \"%s\" not available!" % provider)
        template_name = "ingress/%s.yaml" % provider
        Namespace(name="ingress-nginx").apply()
        Manifest(template_name=template_name).apply()

    def setup_cert(self):
        Namespace(name="cert-manager").apply()
        Manifest(template_name="certificate/cert-manager.yaml").apply()
        Manifest(template_name="certificate/cluster_issuer.yaml").apply()

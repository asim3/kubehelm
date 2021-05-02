from unittest import TestLoader, TextTestRunner
from subprocess import run, PIPE
from sys import exit
# from argparse import ArgumentParser
from k8s.models.manifest import Manifest
from k8s.models.objects import Namespace
from k8s import settings


class RunScriptMixin:
    def _run_script(self, path, *args):
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE)
        return sub_pro.stdout.decode()


class Ingress(RunScriptMixin):
    def __init__(self, **kwargs):
        pass

    def update(self, *args):
        path = settings.BASE_DIR / "scripts/update_ingress.bash"
        print(self._run_script(path, *args))

    def apply(self, provider=None):
        providers = ("do", "aws", "cloud", "kind", "scw", "baremetal")
        if not provider:
            print("providers:", *providers)
            provider = input("provider name: ")
        if not str(provider) in providers:
            raise ValueError("provider \"%s\" not available!" % provider)
        template_name = "ingress/%s.yaml" % provider
        Namespace(name="ingress-nginx").apply()
        Manifest(template_name=template_name).apply()


class Cert(RunScriptMixin):
    def __init__(self, **kwargs):
        pass

    def update(self, *args):
        "update certificate manager"
        path = settings.BASE_DIR / "scripts/update_certificate_manager.bash"
        print(self._run_script(path, *args))

    def apply(self):
        Namespace(name="cert-manager").apply()
        Manifest(template_name="certificate/cert-manager.yaml").apply()
        Manifest(template_name="certificate/cluster_issuer.yaml").apply()

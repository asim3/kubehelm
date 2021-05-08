from k8s.models.manifest import Manifest
from k8s.models.objects import Namespace
from k8s import settings

from .scripts import RunScriptMixin


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
    script_name = "cert_manager.bash"

    def __init__(self, **kwargs):
        pass

    def apply(self):
        print(self._run_script(self.script_name, "install"))
        # Manifest(template_name="cluster_issuer/letsencrypt_staging.yaml").apply()
        # Manifest(template_name="cluster_issuer/letsencrypt_prod.yaml").apply()

    def update(self, *args):
        print(self._run_script(self.script_name, "update"))

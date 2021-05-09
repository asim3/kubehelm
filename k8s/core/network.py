from k8s.models.manifest import Manifest
from k8s.models.objects import Namespace
from k8s import settings

from .scripts import RunScriptMixin


class Ingress(RunScriptMixin):
    script_name = "ingress.bash"

    def __init__(self, **kwargs):
        pass

    def install(self):
        print(self._run_script("install"))

    def update(self, *args):
        print(self._run_script("update"))


class Cert(RunScriptMixin):
    script_name = "cert_manager.bash"

    def __init__(self, **kwargs):
        pass

    def install(self):
        print(self._run_script("install"))
        # Manifest(template_name="cluster_issuer/letsencrypt_staging.yaml").install()
        # Manifest(template_name="cluster_issuer/letsencrypt_prod.yaml").install()

    def update(self, *args):
        print(self._run_script("update"))

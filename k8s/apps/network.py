from k8s.models.scripts import RunScript
from k8s.models.manifest import Manifest


class Ingress(RunScript):
    script_name = "ingress.bash"

    def __init__(self, **kwargs):
        pass

    def install(self):
        print(self.run_script("install"))

    def update(self, *args):
        print(self.run_script("update"))


class Cert(RunScript):
    script_name = "cert_manager.bash"

    def __init__(self, **kwargs):
        pass

    def install(self):
        print(self.run_script("install"))

    def update(self, *args):
        print(self.run_script("update"))


class LetsencryptStaging(Manifest):
    template_name = 'cluster_issuer/letsencrypt_staging.yaml'


class LetsencryptProduction(Manifest):
    template_name = 'cluster_issuer/letsencrypt_prod.yaml'

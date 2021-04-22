from .manifest import ManifestBase


class Whoami(ManifestBase):
    template_name = 'whoami.yaml'
    required_context = ["namespace", "app_name"]

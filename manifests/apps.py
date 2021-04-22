from .manifest import Manifest


class Whoami(Manifest):
    template_name = 'whoami.yaml'
    required_context = ["namespace", "app_name"]

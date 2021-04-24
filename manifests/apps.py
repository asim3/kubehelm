from .manifest import Manifest


class Whoami(Manifest):
    template_name = 'whoami.yaml'
    required_context = ["namespace", "app_name"]


class Wordpress(Manifest):
    template_name = 'wp.yaml'
    required_context = ["namespace", "app_name"]


class Apps:
    whoami = Whoami
    wordpress = Wordpress

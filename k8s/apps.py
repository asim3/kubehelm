from k8s.models.manifest import Manifest
from k8s.core.network import Ingress, Cert


class Django(Manifest):
    template_name = 'apps/django.yaml'
    required_context = ["namespace", "app_name"]


class Whoami(Manifest):
    template_name = 'apps/whoami.yaml'
    required_context = ["namespace", "app_name"]


class Mariadb(Manifest):
    template_name = 'apps/mariadb.yaml'
    required_context = ["namespace", "app_name"]


class Wordpress(Manifest):
    template_name = 'apps/wordpress.1.yaml'
    required_context = ["namespace", "app_name"]


class Manifests:
    whoami = Whoami
    wordpress = Wordpress
    mariadb = Mariadb
    django = Django

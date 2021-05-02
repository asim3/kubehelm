from k8s.models.manifest import Manifest
from k8s.core.network import Ingress, Cert


class Django(Manifest):
    template_name = 'apps/django.yaml'
    required_context = ["namespace", "app_name"]


class Whoami(Manifest):
    template_name = 'apps/whoami.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Whoami",
        "namespace": "default",
        "image_name": "asim3/whoami",
        "image_tag": "1.3",
        "port": 80,
    }


class Mariadb(Manifest):
    template_name = 'apps/mariadb.yaml'
    required_context = ["namespace", "app_name"]


class Wordpress(Manifest):
    template_name = 'apps/wordpress.1.yaml'
    required_context = ["namespace", "app_name"]

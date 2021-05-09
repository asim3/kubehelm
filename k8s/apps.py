from k8s.models.helm import Helm
from k8s.models.manifest import Manifest
from k8s.core.network import Ingress, Cert


class Mariadb(Helm):
    required_context = ["namespace", "app_name"]
    chart_name = "bitnami/mariadb"


class Phpmyadmin(Helm):
    required_context = ["namespace", "app_name"]
    chart_name = "bitnami/phpmyadmin"


class Wordpress(Helm):
    required_context = ["namespace", "app_name"]
    chart_name = "bitnami/wordpress"


class Osclass(Helm):
    required_context = ["namespace", "app_name"]
    chart_name = "bitnami/osclass"


class Django(Manifest):
    template_name = 'apps/django.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Django",
        "namespace": "default",
        "image_name": "asim3/django_test",
        "image_tag": "3.0",
    }


class Whoami(Manifest):
    template_name = 'apps/whoami.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Whoami",
        "namespace": "default",
        "image_name": "asim3/whoami",
        "image_tag": "1.3",
    }

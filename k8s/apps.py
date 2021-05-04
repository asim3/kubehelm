from k8s.models.manifest import Manifest
from k8s.core.network import Ingress, Cert


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


class Mariadb(Manifest):
    template_name = 'apps/mariadb.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Mariadb",
        "namespace": "default",
        "image_name": "docker.io/bitnami/mariadb",
        "image_tag": "10.5.9-debian-10-r28",
    }


class Wordpress(Manifest):
    template_name = 'apps/wp.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Wordpress",
        "namespace": "default",
        "image_name": "docker.io/bitnami/wordpress",
        "image_tag": "5.7.0-debian-10-r11",
    }


class Wordpress2(Manifest):
    template_name = 'apps/wp-bitnami.yaml'
    required_context = []
    default_context = {
        "manifest_name": "Wordpress",
        "namespace": "default",
        "image_name": "wordpress",
        "image_tag": "php8.0-fpm-alpine",
    }


class Phpmyadmin(Manifest):
    template_name = 'apps/phpmyadmin.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "PhpMyAdmin",
        "namespace": "default",
        "image_name": "docker.io/bitnami/phpmyadmin",
        "image_tag": "5.1.0-debian-10-r28",
    }

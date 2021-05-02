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
        "port": 8000,
    }


class Whoami(Manifest):
    template_name = 'apps/whoami.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Whoami",
        "namespace": "default",
        "image_name": "containous/whoami",
        "image_tag": "latest",
        "port": 80,
    }


class Mariadb(Manifest):
    template_name = 'apps/mariadb.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Mariadb",
        "namespace": "default",
        "image_name": "mariadb",
        "image_tag": "latest",
        "port": 3306,
    }


class Wordpress(Manifest):
    template_name = 'apps/wp.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Wordpress",
        "namespace": "default",
        "image_name": "wordpress",
        "image_tag": "php8.0-fpm-alpine",
        "port": 80,
    }


class Phpmyadmin(Manifest):
    template_name = 'apps/phpmyadmin.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "PhpMyAdmin",
        "namespace": "default",
        "image_name": "phpmyadmin",
        "image_tag": "fpm-alpine",
        "port": 80,
    }

from sys import exit

from .base import Manifest


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

    @classmethod
    def _get_manifest(cls, name):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            print(cls._get_all_manifests())
            exit(2)

    @classmethod
    def _get_all_manifests(cls):
        manifests_list = [method for method in dir(cls)
                          if not method.startswith('_')]
        return "manifests are: \n  %s" % ("\n  ".join(manifests_list))

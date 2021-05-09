from unittest import TestLoader, TextTestRunner
# from argparse import ArgumentParser

from k8s import apps
from k8s.models.objects import Namespace, ListK8sObjects
from k8s import settings

from os import system


class Controller:
    def __init__(self, *args):
        command = ""
        for i, arg in enumerate(args[1:], 2):
            command = arg if not command else "%s_%s" % (command, arg)
            method = getattr(self, command, None)
            if method:
                return method(*args[i:])
        self._print_help()

    def _print_help(self):
        for method in self.__dir__():
            if not method.startswith('_'):
                print(method.replace('_', ' '))

    def _get_manifest(self, *args):
        try:
            name = args[0]
            return getattr(apps, name.capitalize())
        except (IndexError, AttributeError) as err:
            manifests_list = "\n  ".join(self._get_all_manifests())
            print("manifests are: \n  %s" % manifests_list)
            print("="*80)
            raise err

    def _get_all_manifests(self):
        return [method for method in dir(apps) if not method.startswith('_')]

    def _get_context(self, manifest):
        context = {}
        if hasattr(manifest, "required_context"):
            for field in manifest.required_context:
                default = manifest.default_context.get(field) or "-"
                value = input('%s (%s): ' % (field, default))
                context[field] = value or default
        return context

    def _add_minikube_link(self, context):
        """
         sudo chmod 644 /etc/hosts; ll /etc/hosts
         sudo chmod 666 /etc/hosts; ll /etc/hosts
        """
        app_name = context.get("app_name")
        system("echo \"$(minikube ip) %s.asim.com\" >> /etc/hosts" % app_name)

    def test(self, *args):
        loader = TestLoader().discover(settings.BASE_DIR / "tests")
        TextTestRunner().run(loader)

    def apply(self, *args):
        manifest = self._get_manifest(*args)
        context = self._get_context(manifest)
        if context.get("namespace") != "default":
            Namespace(name=context.get("namespace")).apply()
        self._add_minikube_link(context)
        results = manifest(**context).apply()
        print(results)

    def list(self, *args):
        print(ListK8sObjects(args[0]).deployments())
        print("="*99)
        print(ListK8sObjects(args[0]).pods())

    def update(self, *args):
        manifest = self._get_manifest(*args)
        results = manifest(**self._get_context(manifest)).update()
        print(results)

    def delete(self, *args):
        manifest = self._get_manifest(*args)
        results = manifest(**self._get_context(manifest)).delete()
        print(results)

from unittest import TestLoader, TextTestRunner
from subprocess import run, PIPE
# from argparse import ArgumentParser

from manifests import apps
from conf import settings


class Command:
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

    def _run_script(self, path, *args):
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE)
        return sub_pro.stdout.decode()

    def test(self, *args):
        loader = TestLoader().discover(settings.BASE_DIR / "tests")
        TextTestRunner().run(loader)

    def apply_whoami(self, *args):
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        apps.Whoami(namespace=namespace, app_name=app_name).apply()

    def apply_wordpress(self, *args):
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        apps.Wordpress(namespace=namespace, app_name=app_name).apply()

    def ingress(self, *args):
        path = settings.BASE_DIR / "scripts/update_ingress.bash"
        print(self._run_script(path, *args))

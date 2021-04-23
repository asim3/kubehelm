from unittest import TestLoader, TextTestRunner
from subprocess import run, PIPE
# from argparse import ArgumentParser

from manifests.apps import Whoami
from conf import settings


class Command:
    def __init__(self, *args):
        if 1 < len(args):
            command = getattr(self, args[1], None)
            if command:
                return command(*args[2:])
        self._print_help()

    def _print_help(self):
        for method in self.__dir__():
            if not method.startswith('_'):
                print(method)

    def _run_script(self, path, *args):
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE)
        return sub_pro.stdout.decode()

    def test(self, *args):
        loader = TestLoader().discover(settings.BASE_DIR / "tests")
        TextTestRunner().run(loader)

    def apply(self, *args):
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        Whoami(namespace=namespace, app_name=app_name).apply()

    def ingress(self, *args):
        path = settings.BASE_DIR / "scripts/update_ingress.bash"
        print(self._run_script(path, *args))

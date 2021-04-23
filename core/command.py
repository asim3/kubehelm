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
        self.print_help()

    def print_help(self):
        for method in self.__dir__():
            if not method.startswith('_') and method != "print_help":
                print(method)

    def test(self, *args):
        loader = TestLoader().discover(settings.BASE_DIR / "tests")
        TextTestRunner().run(loader)

    def apply(self, *args):
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        Whoami(namespace=namespace, app_name=app_name).apply()

    def ingress(self, *args):
        script_path = settings.BASE_DIR / "scripts/update_ingress.bash"
        script = "%s %s" % (script_path, settings.BASE_DIR)
        sub_pro = run([script], shell=True, stdout=PIPE)
        print(sub_pro.stdout.decode())

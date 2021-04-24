from unittest import TestLoader, TextTestRunner
from subprocess import run, PIPE
# from argparse import ArgumentParser

from manifests.apps import Apps
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

    def apply(self, *args):
        try:
            app = getattr(Apps, args[0])
        except AttributeError as err:
            print("apps are:")
            [print(method)
             for method in Apps().__dir__() if not method.startswith('_')]
            print("="*80)
            raise err
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        app(namespace=namespace, app_name=app_name).apply()

    def update_ingress(self, *args):
        path = settings.BASE_DIR / "scripts/update_ingress.bash"
        print(self._run_script(path, *args))

    def update_cert(self, *args):
        "update certificate manager"
        path = settings.BASE_DIR / "scripts/update_certificate_manager.bash"
        print(self._run_script(path, *args))

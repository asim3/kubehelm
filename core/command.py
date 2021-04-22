from unittest import TestLoader, TextTestRunner

from manifests.apps import Whoami
from conf.settings import BASE_DIR


class Command:
    def __init__(self, *args):
        pass

    def test(self):
        loader = TestLoader().discover(BASE_DIR / "tests")
        TextTestRunner().run(loader)

    def apply(self):
        namespace = input('Enter your namespace (default): ') or "default"
        app_name = input('Enter your app name: ')
        Whoami(namespace=namespace, app_name=app_name).apply()

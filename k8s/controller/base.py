from argparse import ArgumentParser

from k8s.models import apps
from k8s.models.objects import ListK8sObjects

import sys
import os


def k8s_list(namespace):
    print(ListK8sObjects(namespace).deployments())
    print("="*99)
    print(ListK8sObjects(namespace).pods())


class Manager:
    actions_list = ['install', 'update', 'delete', 'list']

    def __init__(self):
        self.prog_name = os.path.basename(sys.argv[0])
        if self.prog_name == '__main__.py':
            self.prog_name = 'python -m kubehelm'

    def read_required_context(self, app_class):
        context = {}
        if hasattr(app_class, "required_context") and app_class.required_context:
            for field in app_class.required_context:
                default = app_class.default_context.get(field) or "-"
                value = input('%s (%s): ' % (field, default))
                context[field] = value or default
        return context

    def handle_args(self, nargs):
        if nargs.action == 'list':
            return k8s_list('default')

        try:
            self.app_class = getattr(apps, nargs.app_name.capitalize())
        except (IndexError, AttributeError) as err:
            print("="*80)
            raise err
        context = self.read_required_context(self.app_class)
        app = self.app_class(**context)
        results = getattr(app, nargs.action)()
        print(results)

    def execute(self):
        parser = ArgumentParser(prog=self.prog_name,
                                description='Asim program.')

        parser.add_argument('app_name', help='The app name')
        parser.add_argument('action', choices=self.actions_list)
        parser.add_argument('-n', '--namespace', help='The app name')
        parser.add_argument('-m', '--image', help='The app name')
        parser.add_argument('-t', '--tag', help='The app name')
        self.handle_args(parser.parse_args())

from pathlib import Path
from kubernetes.config import load_kube_config
from kubernetes.client import ApiClient, CoreApi
from kubernetes.client.rest import ApiException
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError

from .template import Template

import json
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent


class Apply:
    template = Template()

    def __init__(self, argv):
        argv.pop(0)
        self.command = argv

    def help(self):
        help_file = open(BASE_DIR / "templates/help.txt", 'r').read()
        print(help_file)

    def execute(self):
        if len(self.command) < 1 or not hasattr(self, self.command[0]):
            self.help()
        else:
            load_kube_config()
            handler = getattr(self, self.command[0])
            handler()

    def get_namespace(self, name):
        return name

    def get_context(self):
        return None

    def render_template(self, path):
        return self.template.render(path, self.get_context())

    def get_template_as_list(self, path):
        return list(yaml.safe_load_all(self.render_template(path)))

    def deploy_new(self, data):
        k8s_client = ApiClient()
        template_as_list = self.get_template_as_list('test')

        failures = []
        for data in template_as_list:
            try:
                create_from_dict(k8s_client, data, dry_run="All")
            except FailToCreateError as failure:
                failures.extend(failure.api_exceptions)

        if failures:
            for fail in failures:
                body = json.loads(fail.body)
                text = "%s[%s]: %s" % (
                    fail.reason, fail.status, body.get('message'))
                print(text)
            print("=" * 80)
            raise FailToCreateError(failures)
        else:
            for data in template_as_list:
                create_from_dict(k8s_client, data)

    def status(self):
        versions = CoreApi().get_api_versions()
        print("version:", versions.versions[0])
        print("kind:", versions.kind)
        print("client_cidr:",
              versions.server_address_by_client_cid_rs[0].client_cidr)
        print("server_address:",
              versions.server_address_by_client_cid_rs[0].server_address)

    def test(self):
        data = {
            "name": "my-dddd-name",
        }

        print(self.render_template('test.yaml'))

        # self.deploy_new(data)

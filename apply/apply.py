from kubernetes.config import load_kube_config
from kubernetes.client import ApiClient, CoreApi
from kubernetes.client.rest import ApiException, ApiValueError
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError

from .template import Template

import json
import yaml


class Apply:
    template = Template()
    template_name = None
    context = None

    def __init__(self):
        load_kube_config()

    def get_context_data(self):
        assert self.context.get('namespace')
        assert self.context.get('app_name')
        return self.context

    def render_template(self):
        return self.template.render(self.template_name, self.get_context_data())

    def get_template_as_list(self):
        self.rendered_template = self.render_template()
        return list(yaml.safe_load_all(self.rendered_template))

    def deploy_new(self):
        k8s_client = ApiClient()
        template_as_list = self.get_template_as_list()

        failures = []
        for data in template_as_list:
            try:
                create_from_dict(k8s_client, data, dry_run="All")
            except FailToCreateError as failure:
                failures.extend(failure.api_exceptions)
            except ApiValueError as err:
                print(self.rendered_template)
                print(err)

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

    def test(self, context):
        self.context = context
        self.template_name = 'test.yaml'
        print(self.render_template())
        # self.deploy_new('test.yaml')

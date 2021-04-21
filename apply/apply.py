from kubernetes.config import load_kube_config
from kubernetes.client import ApiClient, CoreApi
from kubernetes.client.rest import ApiException, ApiValueError
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError

from .template import Template

import json
import yaml


class Apply:
    template = Template()
    extra_context = None
    namespace = None
    app_name = None
    extra_context = None

    def __init__(self):
        load_kube_config()

    def get_context_data(self):
        assert self.namespace
        assert self.app_name

        context = {
            "namespace": self.namespace,
            "app_name": self.app_name
        }
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context

    def render_template(self, path):
        return self.template.render(path, self.get_context_data())

    def get_template_as_list(self, path):
        self.rendered_template = self.render_template(path)
        return list(yaml.safe_load_all(self.rendered_template))

    def deploy_new(self, path):
        k8s_client = ApiClient()
        template_as_list = self.get_template_as_list(path)

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

    def test(self):
        self.namespace = "default"
        self.app_name = "nnnnn"
        self.deploy_new('test.yaml')

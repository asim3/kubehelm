from jinja2.runtime import Context
from kubernetes.config import load_kube_config
from kubernetes.client import ApiClient
from kubernetes.client.rest import ApiException, ApiValueError
from kubernetes.utils.create_from_yaml import create_from_dict, FailToCreateError

from .template import Template

import json
import yaml


class TemplateMixin:
    template_name = None
    context = None
    required_context = ["namespace", "app_name"]

    def render_template(self, context):
        cleaned_context = self.clean_context_data(context)
        return Template().render(self.get_template_name(), cleaned_context)

    def clean_context_data(self, context):
        # TODO: assert is dict
        for key, value in context.items():
            if key in self.required_context:
                if not value:
                    raise ValueError("The value of %s is required" % key)
        return context

    # TODO: clean namespace

    def get_template_name(self):
        if self.template_name is None:
            raise ValueError(
                "TemplateMixin requires a definition of 'template_name'.")
        else:
            return self.template_name


class DeployBase(TemplateMixin):
    context = None

    def __init__(self):
        load_kube_config()

    def get_template_as_list(self):
        self.rendered_template = self.render_template(self.context)
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


class Apply(DeployBase):
    template_name = 'test.yaml'

    def test(self, context):
        self.context = context
        # print(self.render_template(self.context))
        self.deploy_new()

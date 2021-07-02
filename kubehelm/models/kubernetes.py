from kubernetes.client.exceptions import ApiException
from kubernetes.client.models import V1ObjectMeta
from json import loads as json_loads
from inspect import signature


class K8sBaseModel:
    read_class = None
    list_class = None
    apply_class = None
    update_class = None
    delete_class = None
    object_class = None
    spec_class = None
    namespace = None
    name = None
    component = None
    version = None
    managed_by = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_labels(self):
        labels = {
            "app.kubernetes.io/name": self.name,
            "app.kubernetes.io/instance": self.name,
            "app.kubernetes.io/part-of": self.name,
        }
        if self.component:
            labels["app.kubernetes.io/component"] = self.component
        if self.version:
            labels["app.kubernetes.io/version"] = self.version
        if self.managed_by:
            labels["app.kubernetes.io/managed-by"] = self.managed_by
        return labels

    def _get_metadata(self):
        return V1ObjectMeta(
            namespace=self.namespace,
            name=self.name,
            labels=self._get_labels())

    def _get_spec(self):
        if self.spec_class:
            return self.spec_class()

    def _get_manifest_object(self):
        if not self.object_class:
            raise NotImplementedError(
                '%s must set object_class attribute' % self.__class__.__name__)
        return self.object_class(metadata=self._get_metadata(), spec=self._get_spec())

    def _get_args(self, method):
        kwargs = {}
        for arg in signature(method).parameters:
            if arg == 'body':
                kwargs.update({arg: self._get_manifest_object()})
            else:
                value = getattr(self, arg, False)
                if value:
                    kwargs.update({arg: value})
        # print("="*88)
        # print("signature().parameters", signature(method).parameters)
        return kwargs

    def get_replicas(self, status):
        return {
            "replicas": status.get("replicas"),
            "ready_replicas": status.get("ready_replicas"),
        }

    def clean_results(self, response):
        items = getattr(response, 'items', False)
        if items:
            return self.clean_list(items)
        results = response.to_dict()
        return {
            "code": 200,
            "name": results.get("metadata").get("name"),
            "spec": self.clean_spec(results.get('spec')),
            "status": self.clean_status(results.get('status')),
            "namespace": self.namespace,
        }

    def clean_list(self, items):
        results = []
        for item in items:
            results += [self.clean_results(item)]
        return {
            "code": 200,
            "results": results,
        }

    def clean_spec(self, spec):
        return "SSSSSSSS"

    def clean_status(self, status):
        phase = status.get('phase')
        if phase:
            return phase
        replicas = self.get_replicas(status)
        if replicas.get("replicas") and replicas.get("replicas") == replicas.get("ready_replicas"):
            return "Ready Replicas"
        return "TTTTTTTTT"

    def clean_error(self, error):
        if type(error) != dict:
            error = json_loads(error.body)
        return {
            "code": error.get('code'),
            "status": error.get('status'),
            "reason": error.get('reason'),
            "message": error.get('message'),
            "namespace": self.namespace,
        }

    def execute_by_attribute_name(self, attribute_name, **kwargs):
        method = getattr(self, attribute_name, None)
        if not method:
            raise NotImplementedError(
                '%s must set %s attribute before calling get' % (
                    self.__class__.__name__, attribute_name))
        try:
            results = method(**self._get_args(method, **kwargs))
            return self.clean_results(results)
        except ApiException as err:
            return self.clean_error(err)

    def get(self, **kwargs):
        return self.execute_by_attribute_name("get_class", **kwargs)

    def list(self, **kwargs):
        return self.execute_by_attribute_name("list_class", **kwargs)

    def apply(self, **kwargs):
        return self.execute_by_attribute_name("apply_class", **kwargs)

    def update(self, **kwargs):
        return self.execute_by_attribute_name("update_class", **kwargs)

    def delete(self, **kwargs):
        return self.execute_by_attribute_name("delete_class", **kwargs)

    def list_names(self, **kwargs):
        filtered_data = []
        data = self.list(**kwargs)
        items = data.to_dict()
        for obj in items.get('items'):
            filtered_data.append(obj["metadata"]["name"])
        return filtered_data

    def status(self, **kwargs):
        response = self.get(**kwargs)
        return response.get('status')

        # if response.get('code') == 200:
        #     print(response.get('is_list')*8)

        #     if response.get('is_list'):
        #         print("is list"*88)
        #     eee = response.get('status').get('conditions') or []
        #     for a in eee:
        #         print('last_transition_', a.get('last_transition_time'))
        #         print('last_update_time', a.get('last_update_time'))
        #         print('type', a.get('type'))
        #         print('status', a.get('status'))
        #         print('reason', a.get('reason'))
        #         print('message', a.get('message'))
        #         print("--------------")

        # for aa, bb in k8s_model.items():
        #     print("*"*88)
        #     print(aa, "::::::", str(bb)[:100])

        # print("status", k8s_model.get('code'))
        # print("reason", k8s_model.get('reason'))
        # print("message", k8s_model.get('message'))

        # print(sss.phase)
        # print(sss.message)

        # for aa in k8s_model.__dir__():
        #     if not aa.startswith('_'):
        #         bb = getattr(k8s_model, aa, "eeeee")
        #         try:
        #             bb = bb()
        #         except:
        #             pass
        #         print("*"*88)
        #         print(aa, "::::::", str(bb)[:100])

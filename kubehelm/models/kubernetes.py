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

    def clean_spec(self, spec):
        return "EEEEEE"

    def clean_status(self, status):
        phase = status.get('phase')
        if phase:
            return phase
        replicas = status.get("replicas")
        ready_replicas = status.get("ready_replicas")
        if 1 <= replicas:
            if replicas == ready_replicas:
                return "Sustained"
            return "Disordered"
        return "TTTTTTTTT"

    def clean_results(self, response):
        items = getattr(response, 'items', False)
        if type(items) == list:
            return self.clean_list(items)
        results = response.to_dict()
        return {
            "name": results.get("metadata").get("name"),
            # "spec": self.clean_spec(results.get('spec')),
            "status": self.clean_status(results.get('status')),
            "namespace": self.namespace}

    def clean_list(self, items):
        results = []
        for item in items:
            results += [self.clean_results(item)]
        return {"results": results}

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
                '%s must set %s attribute before calling %s' % (
                    self.__class__.__name__, attribute_name, attribute_name[:-6]))
        try:
            results = method(**self._get_args(method, **kwargs))
            clean_results = self.clean_results(results)
            clean_results["code"] = 200
            return clean_results
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
        names = []
        list_data = self.list(**kwargs)
        if list_data.get("code") == 200:
            for data in list_data.get("results"):
                names += [data.get('name')]
        return names

    def status(self, **kwargs):
        response = self.get(**kwargs)
        return response.get('status')

    def is_ready(self, **kwargs):
        ready_status = ['Running', 'Succeeded', 'Sustained']
        if self.status(**kwargs) in ready_status:
            return True
        return False

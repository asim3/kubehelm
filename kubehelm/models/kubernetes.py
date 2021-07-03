from kubernetes.client.exceptions import ApiException
from kubernetes.client.models import V1ObjectMeta
from json import loads as json_loads
from inspect import signature
from time import sleep


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
        return kwargs

    def clean_spec(self, spec):
        return "EEEEEEEE"

    def clean_pod_status(self, container):
        state = getattr(container[0], "state", False)
        if state.terminated:
            return state.terminated.reason
        if state.waiting:
            return state.waiting.reason
        if state.running:
            return "Running"
        return "PPPPPPPP"

    def clean_replicas_status(self, response):
        replicas = getattr(response.spec, "replicas", False)
        if replicas:
            ready_replicas = response.status.ready_replicas or 0
            if 1 <= replicas:
                if replicas == ready_replicas:
                    return "Sustained"
                if replicas < ready_replicas:
                    return "Overload"
                return "Disordered"
        return "RRRRRRRR"

    def clean_status(self, response):
        container = getattr(response.status, "container_statuses", False)
        if container:
            return self.clean_pod_status(container)
        phase = getattr(response.status, "phase", False)
        if phase:
            return phase
        return self.clean_replicas_status(response)

    def clean_is_ready(self, response):
        container = getattr(response.status, "container_statuses", False)
        if container and container[0].ready:
            return True
        phase = getattr(response.status, "phase", False)
        if phase:
            if phase in ["Active", "Succeeded"]:
                return True
        if self.clean_replicas_status(response) in ["Sustained", "Overload"]:
            return True
        return False

    def clean_results(self, results):
        items = getattr(results, 'items', False)
        if type(items) == list:
            return self.clean_list(items)
        return {
            "name": results.metadata.name,
            # "spec": self.clean_spec(results.spec),
            "status": self.clean_status(results),
            "is_ready": self.clean_is_ready(results),
            "namespace": self.namespace}

    def clean_list(self, results):
        data = []
        for item in results:
            data += [self.clean_results(item)]
        return {"results": data}

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
        response = self.get(**kwargs)
        if response.get('code') == 200:
            return response.get('is_ready')
        return False

    def wait(self, **kwargs):
        for _ in range(120):
            if self.is_ready(**kwargs):
                break
            sleep(1)

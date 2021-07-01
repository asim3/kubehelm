from unittest.case import skip
from kubernetes.client.exceptions import ApiException
from kubernetes.client.models import V1ObjectMeta
from json import loads as json_loads
from inspect import signature


class ModelBase:
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
                'subclasses of ModelBase must set object_class attribute')
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
        print(kwargs)
        return kwargs

    def clean_error(self, error):
        body = json_loads(error.body)
        return {
            "status": error.status,
            "reason": error.reason,
            "message": body.get('message')}

    def get(self):
        if not self.read_class:
            raise NotImplementedError(
                'subclasses of ModelBase must set read_class attribute before calling get')
        try:
            return self.read_class(**self._get_args(self.read_class))
        except ApiException as err:
            return self.clean_error(err)

    def list(self):
        if not self.list_class:
            raise NotImplementedError(
                'subclasses of ModelBase must set list_class attribute before calling list')
        try:
            return self.list_class(**self._get_args(self.list_class))
        except ApiException as err:
            return self.clean_error(err)

    def apply(self, dry_run=None):
        if not self.apply_class:
            raise NotImplementedError(
                'subclasses of ModelBase must set apply_class attribute before calling apply')
        try:
            return self.apply_class(**self._get_args(self.apply_class), dry_run=dry_run)
        except ApiException as err:
            return self.clean_error(err)

    def update(self, dry_run=None):
        if not self.update_class:
            raise NotImplementedError(
                'subclasses of ModelBase must set update_class attribute before calling update')
        try:
            return self.update_class(**self._get_args(self.update_class), dry_run=dry_run)
        except ApiException as err:
            return self.clean_error(err)

    def delete(self, dry_run=None):
        if not self.delete_class:
            raise NotImplementedError(
                'subclasses of ModelBase must set delete_class attribute before calling delete')
        try:
            return self.delete_class(**self._get_args(self.delete_class), dry_run=dry_run)
        except ApiException as err:
            return self.clean_error(err)

    def list_names(self, **kwargs):
        filtered_data = []
        data = self.list(**kwargs)
        items = data.to_dict()
        for obj in items.get('items'):
            filtered_data.append(obj["metadata"]["name"])
        return filtered_data

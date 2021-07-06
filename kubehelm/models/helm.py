from json import loads as json_loads
from tempfile import NamedTemporaryFile

from .script import RunScript
from .context import Context
from .template import Template

import os


class Helm(Context, Template, RunScript):
    script_name = "helm.bash"
    chart_name = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.template_name = "%s.yaml" % self.chart_name
        super().__init__(**kwargs)

    def get_args(self):
        assert self.chart_name
        return [
            self.cleaned_data["name"],
            self.cleaned_data["namespace"],
            self.chart_name,
            self.get_values_file_path()]

    def get_values_file_path(self):
        data = self.render(self.cleaned_data)
        with NamedTemporaryFile(delete=False) as file:
            file.write(data.encode('utf-8'))
            # file.seek(0)
            # file.read()
        # delete file using os
        # os.unlink(file.name)
        return file.name

    def as_dict(self, text):
        as_dict = json_loads(text)
        info = as_dict.get('info')
        return {
            'name': as_dict.get('name'),
            'namespace': as_dict.get('namespace'),
            'version': as_dict.get('version'),
            'first_deployed': info.get('first_deployed'),
            'last_deployed': info.get('last_deployed'),
            'description': info.get('description'),
            'status': info.get('status'),
            'deleted': info.get('deleted'),
        }

    def install(self, **kwargs):
        self.pre_install(**kwargs)
        return self.as_dict(self.execute("install", **kwargs))

    def update(self, **kwargs):
        self.pre_update(**kwargs)
        return self.as_dict(self.execute("update", **kwargs))

    def delete(self, **kwargs):
        self.pre_delete(**kwargs)
        return self.execute("delete", **kwargs)

    def execute(self, instruction, **kwargs):
        args = self.get_args()
        if kwargs.get("dry_run", None):
            args.append("--dry-run")
        return self.run_script(instruction, *args)

    def pre_install(self, **kwargs):
        pass

    def pre_update(self, **kwargs):
        pass

    def pre_delete(self, **kwargs):
        pass

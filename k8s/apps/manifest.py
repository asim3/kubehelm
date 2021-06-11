from k8s.models.manifest import Manifest


class Django(Manifest):
    template_name = 'apps/django.yaml'
    required_context = ["namespace", "app_name", "image_name", "image_tag"]
    default_context = {
        "manifest_name": "Django",
        "namespace": "default",
        "image_name": "asim3/django",
        "image_tag": "v1-cairo",
    }


class Whoami(Manifest):
    template_name = 'apps/whoami.yaml'
    required_context = ["namespace", "app_name"]
    default_context = {
        "manifest_name": "Whoami",
        "namespace": "default",
        "image_name": "asim3/whoami",
        "image_tag": "1.3",
        "memory_limit": "128Mi",
        "cpu_limit": "50m",
    }

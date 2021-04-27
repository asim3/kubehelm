from .base import Manifest


class Whoami(Manifest):
    template_name = 'apps/whoami.yaml'
    required_context = ["namespace", "app_name"]


class Wordpress(Manifest):
    template_name = 'apps/wordpress.yaml'
    required_context = ["namespace", "app_name"]


class Manifests:
    whoami = Whoami
    wordpress = Wordpress

    def _get_all_manifests(self):
        manifests_list = [method for method in self.__dir__()
                          if not method.startswith('_')]
        return "manifests are: \n%s" % ("\n".join(manifests_list))

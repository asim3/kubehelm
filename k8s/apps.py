from .manifest import Manifest


class Whoami(Manifest):
    template_name = 'apps/wordpress.yaml'
    required_context = ["namespace", "app_name"]


class Wordpress(Manifest):
    template_name = 'apps/wordpress.yaml'
    required_context = ["namespace", "app_name"]


class Apps:
    whoami = Whoami
    wordpress = Wordpress

    def _get_all_apps(self):
        apps_list = [method for method in self.__dir__()
                     if not method.startswith('_')]
        return "apps are: \n%s" % ("\n".join(apps_list))

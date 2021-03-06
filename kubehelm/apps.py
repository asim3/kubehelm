from kubehelm.models import RunAppScript, Manifest, Helm


class Ingress(RunAppScript):
    script_name = "ingress.bash"
    allowed_methods = ["install", "update"]


class Cert(RunAppScript):
    script_name = "cert_manager.bash"
    allowed_methods = ["install", "update"]


class Issuerstaging(RunAppScript):
    script_name = 'letsencrypt_staging.bash'
    allowed_methods = ["install"]


class Issuerproduction(RunAppScript):
    script_name = 'letsencrypt_production.bash'
    allowed_methods = ["install"]


class Django(Manifest):
    template_name = 'manifests/django.yaml'
    required_context = ["namespace", "name", "image_name", "image_tag"]
    default_context = {
        "manifest_name": "Django",
        "namespace": "default",
        "image_name": "asim3/django",
        "image_tag": "latest",
        "memory_limit": "128Mi",
        "cpu_limit": "50m",
        "secrets": [],
    }


class Whoami(Manifest):
    template_name = 'manifests/whoami.yaml'
    required_context = ["namespace", "name"]
    default_context = {
        "manifest_name": "Whoami",
        "namespace": "default",
        "image_name": "containous/whoami",
        "image_tag": "latest",
        "memory_limit": "128Mi",
        "cpu_limit": "50m",
        "secrets": [],
    }


class Mariadb(Helm):
    required_context = ["namespace", "name", "root_password",
                        "database", "username", "password"]
    chart_name = "bitnami/mariadb"
    default_context = {
        "namespace": "default",
        "name": "staging-production-db",
        "root_password": "root",
        "database": "staging_production_database",
    }


class Phpmyadmin(Helm):
    required_context = ["namespace", "name"]
    chart_name = "bitnami/phpmyadmin"


class Wordpress(Helm):
    required_context = ["namespace", "name"]
    chart_name = "bitnami/wordpress"


class Osclass(Helm):
    required_context = ["namespace", "name"]
    chart_name = "bitnami/osclass"

from subprocess import run, PIPE

from k8s import settings


class RunScriptMixin:
    scripts_base_path = settings.BASE_DIR / "k8s/core/scripts"

    def _run_script(self, script_name, *args):
        path = "%s/%s" % (self.scripts_base_path, script_name)
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE)
        return sub_pro.stdout.decode()

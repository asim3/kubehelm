from subprocess import run, PIPE

from k8s import settings


class RunScriptMixin:
    def _run_script(self, path, *args):
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE)
        return sub_pro.stdout.decode()

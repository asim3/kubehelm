from subprocess import run, PIPE

from k8s import settings


class RunScriptMixin:
    scripts_base_path = settings.BASE_DIR / "k8s/core/scripts"
    script_name = None

    def _run_script(self, *args):
        assert self.script_name
        path = "%s/%s" % (self.scripts_base_path, self.script_name)
        script = "%s %s %s" % (path, settings.BASE_DIR, " ".join(args))
        sub_pro = run([script], shell=True, stdout=PIPE, stderr=PIPE)
        if sub_pro.stderr:
            raise RunScriptError(sub_pro.stderr.decode())
        return sub_pro.stdout.decode()


class RunScriptError(SyntaxError):
    pass

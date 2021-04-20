from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Apply:

    def __init__(self, argv):
        argv.pop(0)
        self.command = argv

    def help(self):
        help_file = open(BASE_DIR / "templates/help.txt", 'r').read()
        print(help_file)

    def execute(self):
        if len(self.command) < 1 or not hasattr(self, self.command[0]):
            self.help()
        else:
            print("execute:", self.command[0])

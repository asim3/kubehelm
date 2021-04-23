#!/usr/bin/env python3

from sys import argv
# from argparse import ArgumentParser

from core.command import Command
from conf import settings

if __name__ == '__main__':
    if len(argv) < 2:
        help_file = open(settings.BASE_DIR / "templates/help.txt", 'r').read()
        print(help_file)
    else:
        command = Command(*argv[2:])
        getattr(command, argv[1])()

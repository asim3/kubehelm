#!/usr/bin/env python3

from sys import argv
# from argparse import ArgumentParser

from core.command import Command
from conf.settings import BASE_DIR


if __name__ == '__main__':
    if len(argv) < 2:
        help_file = open(BASE_DIR / "templates/help.txt", 'r').read()
        print(help_file)
    else:
        print(argv[2:])
        command = Command(*argv[2:])
        getattr(command, argv[1])()

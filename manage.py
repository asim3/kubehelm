#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from manifests.apps import Whoami
# from argparse import ArgumentParser


BASE_DIR = Path(__file__).resolve().parent


# def get_command():
#     argv.pop(0)
#     command = argv

#     if len(command) < 1:
#         help_file = open(BASE_DIR / "templates/help.txt", 'r').read()
#         raise ValueError(help_file)
#     return command[0]


def main():
    # handler = getattr(apply, get_command())

    namespace = input('Enter your namespace (default): ') or "default"
    app_name = input('Enter your app name: ')

    Whoami(namespace=namespace, app_name=app_name).apply()


if __name__ == '__main__':
    main()

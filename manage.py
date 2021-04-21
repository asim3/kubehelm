#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from apply.apply import Apply
# from argparse import ArgumentParser


BASE_DIR = Path(__file__).resolve().parent


def get_command():
    argv.pop(0)
    command = argv

    if len(command) < 1 or not hasattr(Apply, command[0]):
        help_file = open(BASE_DIR / "templates/help.txt", 'r').read()
        raise ValueError(help_file)
    return command[0]


def main():
    """Run an Apply."""
    apply = Apply()
    handler = getattr(apply, get_command())

    namespace = input('Enter your namespace: (default) ')
    app_name = input('Enter your app name: ')

    context = {
        "namespace": namespace,
        "app_name": app_name
    }
    handler(context)


if __name__ == '__main__':
    main()

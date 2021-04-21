#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from apply.apply import Apply


BASE_DIR = Path(__file__).resolve().parent.parent


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
    handler()


if __name__ == '__main__':
    main()

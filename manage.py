#!/usr/bin/env python

from sys import argv
from apply import execute_from_command_line


def main():
    try:
        command = argv[1]
    except IndexError as exc:
        raise ValueError('select a command!') from exc

    execute_from_command_line(command)


if __name__ == '__main__':
    main()

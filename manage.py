#!/usr/bin/env python3

from sys import argv
from k8s.core.command import Command


if __name__ == '__main__':
    Command(*argv)

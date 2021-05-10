#!/usr/bin/env python3

from sys import argv
from k8s.controller.base import Controller


if __name__ == '__main__':
    Controller(*argv)

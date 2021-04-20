#! /usr/bin/python3


class Apply:

    def __init__(self, command):
        self.command = command

    def execute(self):
        print(self.command)

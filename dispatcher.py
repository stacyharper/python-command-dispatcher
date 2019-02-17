#!/bin/python

from sys import exit, argv
from yaml import load
from subprocess import check_call, CalledProcessError

class Printer:
    INFO = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @classmethod
    def print_info(cls, message):
        print(
            cls.INFO
            + message
            + cls.ENDC
        )
    @classmethod
    def print_error(cls, message):
        print(
            cls.FAIL
            + message
            + cls.ENDC
        )
    def build_command_message(command):
        message = '$'
        for argument in command:
            message += ' \'' + argument + '\''
        return message

class Dispatcher:
    def __init__(self, command_file_path):
        content = load(open(command_file_path))
        self.commands = content['commands']

    def run(self, command_event):
        if None == self.commands:
            return
        if command_event not in self.commands:
            return

        commands = self.commands[command_event]
        for command in commands:
            Printer.print_info(Printer.build_command_message(command))
            check_call(command)


if __name__ == '__main__':
    framework = Dispatcher(argv[2])
    try:
        framework.run(argv[1])
    except FileNotFoundError as e:
        Printer.print_error(e.args[1])
        exit(1)
    except CalledProcessError as e:
        Printer.print_error('Returned ' + str(e.returncode))
        exit(e.returncode)

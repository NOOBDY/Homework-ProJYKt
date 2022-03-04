#!/usr/bin/env python
import json
from typing import Dict, Tuple
from sys import argv, exit

from cmd import Cmd

import urllib3
from requests.exceptions import ConnectTimeout, SSLError
from urllib3.exceptions import InsecureRequestWarning

from utils import JykuoSession
from utils.setup import setup

urllib3.disable_warnings(category=InsecureRequestWarning)


class Colors:
    DEFAULT = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


class TestException(Exception):
    pass
class ConfigNotFound(Exception):
    pass
...


def loadConfig():
    try:
        with open("./config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise ConfigNotFound


def exceptionProcess(oldFunc):
    def newFunc(*arg, **kwarg):
        try:
            oldFunc(*arg, **kwarg)
        except TestException:
            print('dont mind, just test')
        except ConfigNotFound:
            print("Not yet setup yet")
        except ConnectTimeout:
            print("Not connected to school network")
        except SSLError:
            print("Wrong username or password")
        except FileNotFoundError:
            print("Submitted File Not Found")
    return newFunc


class HwpShell(cmd.Cmd):
    prompt = "[hwp] "

    def __enter__(self):
        return self
    def __exit__(self):
        self.session.close()
    def __init__(self):
        super().__init__()
        self.onecmd = exceptionProcess(self.onecmd)

    def do_get(self, args):
        if args[0] == 'all':
            ...
        else:
            ...
    def do_submit(self, args):
        ...
    def do_setup(self, args):
        ...

    def do_quit(self, args):
        raise SystemExit
    def emptyline(self):
        self.do_help('')
    def default(self, line):
        aliases = {
            'q': self.do_quit,
            'e': self.do_quit,
            'exit': self.do_quit,
            'set': self.do_setup,
            }
        cmd, args, line = self.parseline(line)
        if cmd in aliases:
            aliases[cmd](args)
        else:
            super().default(line)


if __name__ == "__main__":
    try:
        config = loadConfig()
    except ConfigNotFound:
        config = None

    if len(argv) != 1:
        if argv[1] == 'setup':
            HwpShell.onecmd('setup')
        elif not config:
            print("Not yet setup yet")
        else:
            with HwpShell() as shell:
                shell.session = JykuoSession(config)
                shell.onecmd(' '.join(argv[1:]))
        exit()

    while True:
        if not config:
            HwpShell.onecmd('setup')
        with HwpShell() as shell:
            shell.session = JykuoSession(config)
            shell.cmdloop()


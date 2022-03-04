#!/usr/bin/env python
import json
from typing import Dict, Tuple
from sys import argv, exit
from os import path

import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

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


def show_status(question_status: dict, test_status: Dict[str, Tuple[bool, str]]) -> None:
    r_scolor =\
        Colors.GREEN if question_status['release_status'] == "Open" else\
        Colors.YELLOW if question_status['release_status'] == "Preparing" else\
        Colors.RED

    print(
        f"Realese Status: {r_scolor}{question_status['release_status']}{Colors.DEFAULT}, Due: {question_status['due_date']}")
    print("Test Status:")
    if len(test_status) != 0:
        passed = 0
        failed = 0

        for case in test_status:
            if test_status[case][0]:
                print(f" Case {case} {Colors.GREEN}v{Colors.DEFAULT}")
                passed += 1

            else:
                print(f" Case {case} {Colors.RED}x{Colors.DEFAULT}")
                print(f"  {test_status[case][1]}".replace(":", ":\n").replace("\n", "\n    "))
                failed += 1

        print(f"{Colors.GREEN}{passed} passed, {Colors.RED}{failed} failed, {Colors.DEFAULT}{len(test_status)} total")
    else:
        print(" Not Submit Yet")


def loadConfig():
    with open("./config.json", "r") as file:
        login_data = json.load(file)
        base_url = login_data.pop("base_url")
    return login_data, base_url


def exceptionProcess(oldFunc):
    def newFunc(*arg, **kwarg):
        try:
            oldFunc(*arg, **kwarg)
        except ConnectTimeout:
            print("Not connected to school network")
        except SSLError:
            print("Wrong username or password")
        except FileNotFoundError:
            print("Submitted File Not Found")
    return newFunc


class HwpShell(Cmd):
    prompt = "[hwp] "

    def __init__(self):
        super().__init__()
        self.onecmd = exceptionProcess(self.onecmd)

    def do_get(self, args):
        args = args.split()
        if args[0] == 'all':
            question_statuses = self.session.get_question_statuses()
            print(
                f"Index  Realease Status  {'Due Date':<17}  Submit Status")
            for key in question_statuses:
                a = question_statuses[key]
                print(
                    f"{key:>5}  {a['release_status']:<15}  {a['due_date']:<17}  {a['submit_status']}")
        else:
            index = args[0].rjust(2, '0')
            content = self.session.get(index)
            questions_status = self.session.get_question_statuses()[index]
            test_status = self.session.get_test_status(self.student_id, index)
            print(content)
            print("-" * 50)
            show_status(questions_status, test_status)
    def do_submit(self, args):
        args = args.split()
        index = args[0].rjust(2, '0')
        file_path = path.expanduser(args[1])
        questions_status = self.session.get_question_statuses()[index]
        if questions_status['release_status'] == "Closed":
            print("The question has closed, "
                  "submitting the file anyways will delete the uploaded file "
                  "but won't upload your local file."
                  "Do you wish to continue? [y/N]", end='')
            if input() != "y":
                print("Aborting")
                return
        self.session.delete(index)
        self.session.submit(index, file_path)
        print("Submit success.")
        questions_status = self.session.get_question_statuses()[index]
        test_status = self.session.get_test_status(self.student_id, index)
        print("-" * 50)
        show_status(questions_status, test_status)
        
    def do_setup(self, args):
        setup()

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
        login_data, base_url = loadConfig()
    except FileNotFoundError:
        login_data = None

    if len(argv) != 1:
        if argv[1] == 'setup':
            HwpShell().onecmd('setup')
        elif not login_data:
            print("Not yet setup yet")
        else:
            shell = HwpShell()
            shell.session = JykuoSession(base_url)
            shell.session.login(login_data)
            shell.student_id = login_data['name']
            shell.onecmd(' '.join(argv[1:]))
            shell.session.close()
        exit()

    while True:
        if not login_data:
            HwpShell().onecmd('setup')
            login_data, base_url = loadConfig()
        shell = HwpShell()
        shell.session = JykuoSession(base_url)
        shell.session.login(login_data)
        shell.student_id = login_data['name']
        shell.cmdloop()
        shell.session.close()


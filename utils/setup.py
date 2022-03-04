import json
from getpass import getpass
from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import ConnectTimeout

def listOptions():
    print("Option of Courses:")

    try:
        r = Session().get(f"https://140.124.181.36/upload/Login", verify=False, timeout=1)
    except ConnectTimeout:
        print("    Not connected to school network")
        return

    soup = BeautifulSoup(r.content.decode(), "html5lib")
    for test in soup.find("select").find_all("option"):
        print(f"    {test['value']}){test.string}")


def load():
    try:
        with open("./config.json", "r") as file:
            config = json.load(file)
    except:
        config = {"name": "",
                  "passwd": "",}
    return config


def setup(list_options=True):
    config = load()

    config["name"] = id_ =input(f"學號: ") or config["name"]
    config["passwd"] = getpass(f"密碼: ") or config["passwd"]
    if list_options:
        listOptions()
    config["rdoCourse"] = input("Course(default=5): ") or "5"
    config["base_url"] = f"https://140.124.181.{'36' if int(id_[-3:]) % 2 == 1 else '39'}/upload"

    with open("./config.json", "w+") as file:
        file.writelines(json.dumps(config, indent=4))

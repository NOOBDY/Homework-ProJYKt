from typing import Dict, List, Tuple

import urllib3
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


def _get_test_status(self, id_: int, index: str) -> Dict[str, Tuple[bool, str]]:
    session = self.session
    base_url = self.base_url

    # you can check other people's upload status while logged in lol
    res = session.get(
        f"{base_url}/CheckResult?questionID={index}&studentID={id_}")

    soup = BeautifulSoup(res.content.decode(), "html5lib")

    cases: Dict[str, Tuple[bool, str]] = {}
    for test in list(soup.find_all("tr"))[1:]:
        result: List[str] = [i.get_text().strip() for i in test.find_all("td")] # a more bullerproof way to write this
                                                                                # in case something else gets added in the the future
        case: str = result[0]
        status: bool = result[1] == '通過測試'
        output: str = result[2]

        cases[case] = status, output

    return cases

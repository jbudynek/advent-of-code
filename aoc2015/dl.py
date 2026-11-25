import datetime
import os
import sys

import requests  # type: ignore
from dotenv import load_dotenv

load_dotenv()
session_token = os.getenv("SESSION_TOKEN")

y = datetime.datetime.now().year
d = datetime.datetime.now().day
if len(sys.argv) > 1:
    y = int(sys.argv[1])
if len(sys.argv) > 2:
    d = int(sys.argv[2])

url = f"https://adventofcode.com/{y}/day/{d}/input"

response = requests.get(url, cookies={"session": session_token})

if response.status_code == 200:
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, "input.txt")

    with open(path_to_file, "w") as f:
        f.write(response.text)
    print("OK", url, path_to_file)
else:
    print("FAIL", response)

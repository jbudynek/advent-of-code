import os

import requests  # type: ignore
from dotenv import load_dotenv

load_dotenv()
session_token = os.getenv("SESSION_TOKEN")

url = "https://adventofcode.com/2024/day/1/input"

response = requests.get(url, cookies={"session": session_token})

if response.status_code == 200:
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, "input.txt")

    with open(path_to_file, "w") as f:
        f.write(response.text)
    print("OK")
else:
    print("FAIL", response)

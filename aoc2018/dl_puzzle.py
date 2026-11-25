import datetime
import os
import sys

import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from dotenv import load_dotenv

# Usage: python dl_puzzle.py [year] [day] [part]
# Downloads the text of one puzzle part (using SESSION_TOKEN from .env)
# and saves it to puzzle_<year>_<day>_<part>.txt next to this script.

load_dotenv()
session_token = os.getenv("SESSION_TOKEN")
if not session_token:
    sys.exit("FAIL SESSION_TOKEN not found in .env")

y = datetime.datetime.now().year
d = datetime.datetime.now().day
part = 1
if len(sys.argv) > 1:
    y = int(sys.argv[1])
if len(sys.argv) > 2:
    d = int(sys.argv[2])
if len(sys.argv) > 3:
    part = int(sys.argv[3])
if part not in (1, 2):
    sys.exit("FAIL part must be 1 or 2")

url = f"https://adventofcode.com/{y}/day/{d}"
response = requests.get(url, cookies={"session": session_token})
if response.status_code != 200:
    sys.exit(f"FAIL {response}")

soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("article", class_="day-desc")
if part > len(articles):
    sys.exit(
        f"FAIL part {part} not available ({len(articles)} part(s) visible): "
        "part 1 must be solved on the account first, or the session is invalid"
    )

blocks = []
for el in articles[part - 1].find_all(["h2", "p", "pre", "ul", "ol"], recursive=False):
    if el.name in ("ul", "ol"):
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            bullet = f"{i}." if el.name == "ol" else "-"
            blocks.append(f"{bullet} {li.get_text()}")
    else:
        blocks.append(el.get_text().rstrip("\n"))
text = "\n\n".join(blocks) + "\n"

script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_file = os.path.join(script_dir, f"puzzle_{y}_{d}_{part}.txt")
with open(path_to_file, "w") as f:
    f.write(text)
print("OK", url, path_to_file)

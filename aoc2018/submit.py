import datetime
import os
import sys

import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from dotenv import load_dotenv

# Usage:
#   python submit.py <part> <answer>                 (year and day = today)
#   python submit.py <year> <day> <part> <answer>
# Submits the answer (using SESSION_TOKEN from .env) and prints the verdict.
# Warning: no confirmation, and wrong answers trigger a cooldown on the site.

load_dotenv()
session_token = os.getenv("SESSION_TOKEN")
if not session_token:
    sys.exit("FAIL SESSION_TOKEN not found in .env")

args = sys.argv[1:]
if len(args) == 2:
    y = datetime.datetime.now().year
    d = datetime.datetime.now().day
    part, answer = int(args[0]), args[1]
elif len(args) == 4:
    y, d, part, answer = int(args[0]), int(args[1]), int(args[2]), args[3]
else:
    sys.exit(__doc__ or "bad arguments")
if part not in (1, 2):
    sys.exit("FAIL part must be 1 or 2")

url = f"https://adventofcode.com/{y}/day/{d}/answer"
response = requests.post(
    url,
    cookies={"session": session_token},
    data={"level": part, "answer": answer},
)
if response.status_code != 200:
    sys.exit(f"FAIL {response}")

soup = BeautifulSoup(response.text, "html.parser")
main = soup.find("main")
message = " ".join(main.get_text().split()) if main else response.text.strip()
lower = message.lower()

if "that's the right answer" in lower:
    verdict = "CORRECT"
elif "already complete it" in lower:
    verdict = "ALREADY SOLVED"
elif "too high" in lower:
    verdict = "WRONG (too high)"
elif "too low" in lower:
    verdict = "WRONG (too low)"
elif "not the right answer" in lower:
    verdict = "WRONG"
elif "too recently" in lower:
    verdict = "TOO RECENT (wait before retrying)"
else:
    verdict = "UNKNOWN"

print(f"{verdict} - {y} day {d} part {part} answer {answer}")
print(message)

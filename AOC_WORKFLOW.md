# Advent of Code workflow (any year, any day)

Replace `YYYY` and `D` below. All commands run from the year folder `aocYYYY/`.
Tools (same folder): `dl.py` (input), `dl_puzzle.py` (puzzle text), `submit.py` (answers).
All three read `SESSION_TOKEN` from `.env`.

## Rules

- **Gates:** show each command (download, fetch puzzle, submit) and wait for approval before running it.
- **Imports:** keep them minimal. `networkx`, `re`, `numpy`, `shapely`, `collections`, `maths`, `itertools`, `functools` are allowed when needed.
- **Self-contained:** puzzles are almost always self-contained. Do not fetch or reuse earlier days
  unless the current text cannot be solved without it; if so, ask first.
- **No commits:** commits are done separately by the user.
- **Stop on failure:** if a test fails or a submission is not CORRECT, report it and stop.
  Wrong answers trigger a cooldown on the site, so never retry blindly.

## Steps

0. **Check tools.** Make sure `dl.py`, `dl_puzzle.py` and `submit.py` exist in `aocYYYY/`
   (copy them from `aoc2017/` if missing). `.env` must contain `SESSION_TOKEN`.
1. **Download the input** (overwrites `aocYYYY/input.txt`, which is gitignored):
   `cd aocYYYY && python dl.py YYYY D`
2. **Download part 1 text** (saved to `puzzle_YYYY_D_1.txt`, gitignored):
   `python dl_puzzle.py YYYY D 1`, then read it.
3. **Write `dD.py`** (zero-padded, e.g. `d07.py`) with:
   - a header comment: "Algorithm (code written by Claude, an AI assistant made by Anthropic)",
     in English, explaining the big idea;
   - `ipt_test` from the puzzle example and `ipt_puzzle = open("input.txt").read().strip()`;
   - the solution functions;
   - asserts on the example's expected answers, before touching the real input.
4. **Run it** (`python dD.py`), fix until the tests pass, then show the part 1 answer
   and explain the big idea.
5. **Submit part 1:** `python submit.py YYYY D 1 <answer>`.
   If not CORRECT: tell the user and stop.
6. **Download part 2 text:** `python dl_puzzle.py YYYY D 2`, then read it.
7. **Extend `dD.py`:** add part 2 solution and example test, update the header
   with part 2's big idea, run it, show the answer and explain the big idea.
8. **Submit part 2:** `python submit.py YYYY D 2 <answer>`, report the result.
9. **Finish:** append the results as comments at the end of `dD.py`:
   ```
   # Part 1 solution: <answer>
   # Part 2 solution: <answer>
   ```

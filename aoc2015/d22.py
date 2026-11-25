# Algorithm (code written by Claude, an AI assistant made by Anthropic):
# Wizard duel simulated round by round (one player turn + one boss turn).
# State = (player hp, mana, boss hp, shield timer, poison timer, recharge timer).
# - Effects are applied at the start of each turn (player's and boss'), then
#   their timers decrease. Shield gives 7 armor while its timer is > 0 at the
#   start of the boss' turn.
# - A round: apply effects, check boss death, cast a spell (must be affordable and
#   not already active), check boss death, then boss turn: apply effects, check
#   boss death, boss hits for max(1, damage - armor), check player death.
# - Part 1: depth-first search over every possible sequence of spells, keeping the
#   smallest total mana spent among winning fights. Branches are pruned as soon as
#   the mana spent reaches the best known win (spent strictly grows each round, so
#   the search ends).
# - Part 2: hard mode. Same search, but at the very start of each player turn
#   (before effects) the player loses 1 hp, and loses the fight if hp reaches 0.

ipt_test = """Hit Points: 13
Damage: 8"""

ipt_puzzle = open("input.txt").read().strip()

# name: (cost, damage, heal, shield turns, poison turns, recharge turns)
SPELLS = {
    "M": (53, 4, 0, 0, 0, 0),
    "D": (73, 2, 2, 0, 0, 0),
    "S": (113, 0, 0, 6, 0, 0),
    "P": (173, 0, 0, 0, 6, 0),
    "R": (229, 0, 0, 0, 0, 5),
}


def parse(ipt):
    return [int(line.split(":")[1]) for line in ipt.splitlines()]


def effects(st):
    php, mana, bhp, s, p, r = st
    armor = 7 if s > 0 else 0
    if s > 0:
        s -= 1
    if p > 0:
        bhp -= 3
        p -= 1
    if r > 0:
        mana += 101
        r -= 1
    return (php, mana, bhp, s, p, r), armor


def play_round(st, spell, bdmg, hard=False):
    """Returns (result, new state): result is 'win', 'lose' or None (fight goes on)."""
    if hard:
        st = (st[0] - 1,) + st[1:]
        if st[0] <= 0:
            return "lose", st
    st, _ = effects(st)
    if st[2] <= 0:
        return "win", st
    php, mana, bhp, s, p, r = st
    cost, dmg, heal, ts, tp, tr = SPELLS[spell]
    if cost > mana or (ts and s) or (tp and p) or (tr and r):
        return "lose", st
    mana -= cost
    bhp -= dmg
    php += heal
    s, p, r = s or ts, p or tp, r or tr
    if bhp <= 0:
        return "win", (php, mana, bhp, s, p, r)
    st, armor = effects((php, mana, bhp, s, p, r))
    if st[2] <= 0:
        return "win", st
    php = st[0] - max(1, bdmg - armor)
    st = (php,) + st[1:]
    if php <= 0:
        return "lose", st
    return None, st


def min_mana(php, mana, bhp, bdmg, hard=False):
    best = [10**9]

    def dfs(st, spent):
        for spell in SPELLS:
            sp = spent + SPELLS[spell][0]
            if sp >= best[0]:
                continue
            res, nst = play_round(st, spell, bdmg, hard)
            if res == "win":
                best[0] = sp
            elif res is None:
                dfs(nst, sp)

    dfs((php, mana, bhp, 0, 0, 0), 0)
    return best[0]


def run_sequence(php, mana, bhp, bdmg, spells, hard=False):
    st = (php, mana, bhp, 0, 0, 0)
    for sp in spells:
        res, st = play_round(st, sp, bdmg, hard)
        if res:
            return res
    return None


# test: the two fights described in the puzzle (player 10 hp, 250 mana)
assert run_sequence(10, 250, 13, 8, "PM") == "win"
assert run_sequence(10, 250, 14, 8, "RSDPM") == "win"
print("# Test part 1: both example fights are won")
# test part 2: in hard mode the first example fight (Poison, Magic Missile) is lost:
# 10 hp -1 = 9, boss hits 8 -> 1 hp, then -1 at the next turn -> 0 hp
assert run_sequence(10, 250, 13, 8, "PM", hard=True) == "lose"
print("# Test part 2: first example fight is lost in hard mode")

bhp, bdmg = parse(ipt_puzzle)
r1 = min_mana(50, 500, bhp, bdmg)
print(f"# Part 1 solution: {r1}")
r2 = min_mana(50, 500, bhp, bdmg, hard=True)
print(f"# Part 2 solution: {r2}")

# Part 1 solution: 1824
# Part 2 solution: 1937

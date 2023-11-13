# coding: utf-8
import re
from timeit import default_timer as timer

# Main function
##########
# Part 1 = just play the game
# Part 2 = memoization + recursion


def next_dice(dice):
    dice += 1
    if dice == 101:
        dice = 1
    return dice


def boom_part1(input_val, DBG=True):
    pos_player_1 = int(re.findall(r"-?\d+", input_val[0])[1]) - 1
    pos_player_2 = int(re.findall(r"-?\d+", input_val[1])[1]) - 1

    turn = 0
    dice = 0
    score_player_1 = 0
    score_player_2 = 0
    while True:
        turn += 1

        roll_player_1 = 0
        for _ in range(3):
            dice = next_dice(dice)
            roll_player_1 += dice

        pos_player_1 = (pos_player_1 + roll_player_1) % 10
        score_player_1 += pos_player_1 + 1

        if score_player_1 >= 1000:
            return (6 * turn - 3) * score_player_2

        roll_player_2 = 0
        for _ in range(3):
            dice = next_dice(dice)
            roll_player_2 += dice

        pos_player_2 = (pos_player_2 + roll_player_2) % 10
        score_player_2 += pos_player_2 + 1

        if score_player_2 >= 1000:
            return (6 * turn) * score_player_1


def play_turns(
    score_player_1,
    score_player_2,
    pos_player_1,
    pos_player_2,
    player_1_plays,
    state_of_universe,
):

    if (
        score_player_1,
        pos_player_1,
        score_player_2,
        pos_player_2,
        player_1_plays,
    ) in state_of_universe:
        return state_of_universe[
            (score_player_1, pos_player_1, score_player_2, pos_player_2, player_1_plays)
        ]

    else:
        if score_player_1 >= 21:
            return 1, 0
        if score_player_2 >= 21:
            return 0, 1

        total_wins_player_1 = 0
        total_wins_player_2 = 0

        new_score_player_1 = score_player_1
        new_pos_player_1 = pos_player_1
        new_score_player_2 = score_player_2
        new_pos_player_2 = pos_player_2

        for roll1 in range(1, 4):
            for roll2 in range(1, 4):
                for roll3 in range(1, 4):
                    total_roll = roll1 + roll2 + roll3

                    if player_1_plays:
                        new_pos_player_1 = (pos_player_1 + total_roll) % 10
                        new_score_player_1 = score_player_1 + new_pos_player_1 + 1

                        wins_player_1, wins_player_2 = play_turns(
                            new_score_player_1,
                            score_player_2,
                            new_pos_player_1,
                            pos_player_2,
                            not player_1_plays,
                            state_of_universe,
                        )
                        state_of_universe[
                            (
                                new_score_player_1,
                                new_pos_player_1,
                                score_player_2,
                                pos_player_2,
                                not player_1_plays,
                            )
                        ] = (wins_player_1, wins_player_2)
                    else:
                        new_pos_player_2 = (pos_player_2 + total_roll) % 10
                        new_score_player_2 = score_player_2 + new_pos_player_2 + 1

                        wins_player_1, wins_player_2 = play_turns(
                            score_player_1,
                            new_score_player_2,
                            pos_player_1,
                            new_pos_player_2,
                            not player_1_plays,
                            state_of_universe,
                        )
                        state_of_universe[
                            (
                                score_player_1,
                                pos_player_1,
                                new_score_player_2,
                                new_pos_player_2,
                                not player_1_plays,
                            )
                        ] = (wins_player_1, wins_player_2)

                    total_wins_player_1 += wins_player_1
                    total_wins_player_2 += wins_player_2
        return (total_wins_player_1, total_wins_player_2)


def boom_part2(input_val, DBG=True):
    pos_player_1 = int(re.findall(r"-?\d+", input_val[0])[1]) - 1
    pos_player_2 = int(re.findall(r"-?\d+", input_val[1])[1]) - 1

    state_of_universe = {}
    ret = play_turns(0, 0, pos_player_1, pos_player_2, True, state_of_universe)

    return max(ret)


# Testing and timing
##########


def print_time(t_start, t_end):
    s = t_end - t_start
    print(int(s * 1000), "ms = ", int(s), "s = ", int(s / 60), "min")


RED_FG = "\x1b[91m"
GREEN_FG = "\x1b[92m"
YELLOW_FG = "\x1b[93m"
DEFAULT_FG = "\x1b[39m"


def output_test(cc, t_start, t_end, result, expected):
    result = str(result)
    expected = str(expected)
    flag = result == expected
    sflag = ""
    if flag:
        sflag = GREEN_FG + str(flag) + DEFAULT_FG
    else:
        sflag = RED_FG + str(flag) + DEFAULT_FG

    if expected == "None":
        print("*** " + str(cc) + " *** -> Result = " + str(result))
    else:
        print(
            "*** "
            + str(cc)
            + " *** -> Result = "
            + str(result)
            + " -> success = "
            + sflag
            + " -> expected "
            + expected
        )
    print_time(t_start, t_end)
    return flag


def test_part1(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part1(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


def test_part2(cc=None, expected=None, DBG=False):
    t_start = timer()
    result = boom_part2(cc, DBG)
    t_end = timer()

    return output_test(cc, t_start, t_end, result, expected)


# Test cases
##########


tt1 = """Player 1 starting position: 4
Player 2 starting position: 8"""
tt1 = tt1.splitlines()  # type: ignore
test_part1(tt1, 739785, True)
test_part2(tt1, 444356092776315, True)
# sys.exit()

# Real data
##########

INPUT_FILE = "input-d21.txt"
f = open(INPUT_FILE, "r")
contents = f.read()
puzzle_input = contents.splitlines()
f.close()

# part 1

t_start = timer()
ret = boom_part1(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# part 2

t_start = timer()
ret = boom_part2(puzzle_input, DBG=False)
t_end = timer()
print_time(t_start, t_end)
print(ret)

# PART 1 OK = 428736
# PART 2 OK = 57328067654557

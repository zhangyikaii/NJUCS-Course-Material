"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.

    >>> fixed_dice = make_test_dice(3, 4, 1)
    >>> roll_dice(2, dice=fixed_dice)
    7
    >>> roll_dice(2, dice=fixed_dice)
    1
    >>> roll_dice(2, dice=fixed_dice)
    1
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total = 0
    has_one = False
    for _ in range(num_rolls):
        point = dice()
        if point == 1:
            has_one = True
        total += point
    if has_one:
        return 1
    return total
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.

    >>> free_bacon(4)
    3
    >>> free_bacon(1)
    2
    >>> free_bacon(20)
    9
    >>> free_bacon(45)
    13
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    alter_diff = 0
    digits = score ** 3
    do_plus = True
    while digits > 0:
        if do_plus:
            alter_diff += digits % 10
        else:
            alter_diff -= digits % 10
        do_plus = not do_plus
        digits //= 10
    return 1 + abs(alter_diff)
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.

    >>> take_turn(2, 0, make_test_dice(4, 5, 1))
    9
    >>> take_turn(3, 0, make_test_dice(4, 6, 1))
    1
    >>> take_turn(0, 56)
    13
    >>> take_turn(0, 47)
    6
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return free_bacon(opponent_score)
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped

    >>> is_swap(2, 4)
    False
    >>> is_swap(11, 1)
    False
    >>> is_swap(1, 0)
    True
    >>> is_swap(23, 4)
    True
    """
    # BEGIN PROBLEM 4
    excitement = 3 ** (player_score + opponent_score)
    lowest_digit = excitement % 10
    while excitement >= 10:
        excitement //= 10
    highest_digit = excitement
    return highest_digit == lowest_digit
    # END PROBLEM 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence, feral_hogs=True):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    feral_hogs: A boolean indicating whether the feral hogs rule should be active.

    >>> # We recommend working this out turn-by-turn on a piece of paper (use `python` for difficult calculations).
    >>> always_seven = make_test_dice(7)
    >>> strat0 = lambda score, opponent: opponent % 10
    >>> strat1 = lambda score, opponent: max((score // 10) - 4, 0)
    >>> s0, s1 = play(strat0, strat1, score0=71, score1=80, dice=always_seven, feral_hogs=False)
    >>> s0
    78
    >>> s1
    108
    >>> def strat0(s0, s1):
    ...     if s0 == 0: return 3
    ...     if s0 == 7: return 5
    ...     return 8
    >>> def strat1(s0, s1):
    ...     if s0 == 0: return 1
    ...     if s0 == 4: return 2
    ...     return 6
    >>> test_dice = make_test_dice(2, 2, 3, 4, 2, 2, 2, 2, 2, 3, 5, 2, 2, 2, 2, 2, 2, 2, 6, 1)
    >>> s0, s1 = play(strat0, strat1, score0=0, score1=0, goal=21, dice=test_dice) # Test problem 5b.
    >>> s0
    43
    >>> s1
    15
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    last_point0 = 0
    last_point1 = 0
    while score0 < goal and score1 < goal:
        if who == 0:
            num_rolls = strategy0(score0, score1)
            if feral_hogs and abs(num_rolls - last_point0) == 2:
                score0 += 3
            point0 = take_turn(num_rolls, score1, dice)
            score0 += point0
            last_point0 = point0
        else:
            num_rolls = strategy1(score1, score0)
            if feral_hogs and abs(num_rolls - last_point1) == 2:
                score1 += 3
            point1 = take_turn(num_rolls, score0, dice)
            score1 += point1
            last_point1 = point1
        if is_swap(score0, score1):
            score0, score1 = score1, score0
        say = say(score0, score1)
        who = other(who)
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(prev_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != prev_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 17)
    Player 0 now has 6 and Player 1 now has 17
    Player 1 takes the lead by 11
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, prev_high=0, prev_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 11)
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 11)
    >>> f4 = f3(13, 20)
    >>> f5 = f4(20, 35)
    15 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
    >>> f7 = f6(21, 47)
    >>> f8 = f7(21, 77)
    30 point(s)! That's the biggest gain yet for Player 1
    >>> f9 = f8(77, 22) # Swap!
    >>> f10 = f9(33, 77) # Swap!
    55 point(s)! That's the biggest gain yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7

    def say(score0, score1):
        if who == 0:
            chosen_score = score0
        else:
            chosen_score = score1
        new_high = chosen_score - prev_score
        if new_high > prev_high:
            print("{} point(s)! That's the biggest gain yet for Player {}".format(
                new_high, who))
            return announce_highest(who, new_high, chosen_score)
        return announce_highest(who, prev_high, chosen_score)
    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(g, num_samples=1000):
    """Return a function that returns the average value of G when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def averaged(*args):
        total = 0
        for _ in range(num_samples):
            total += g(*args)
        return total / num_samples
    return averaged
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    averaged_roll_dice = make_averaged(roll_dice, num_samples)
    max_avg, max_num_rolls = 0, 0
    for num_rolls in range(1, 11):
        avg = averaged_roll_dice(num_rolls, dice)
        if avg > max_avg:
            max_avg, max_num_rolls = avg, num_rolls
    return max_num_rolls
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 9, margin=8, num_rolls=5)
    0
    >>> bacon_strategy(9, 0, margin=6, num_rolls=5)
    5
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) >= margin:
        return 0
    return num_rolls
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.

    >>> swap_strategy(1, 19, 8, 6)
    0
    >>> swap_strategy(24, 1, 1, 6)
    6
    >>> swap_strategy(13, 18, 1, 6)
    0
    >>> swap_strategy(30, 54, 7, 6)
    6
    """
    # BEGIN PROBLEM 11
    gain = free_bacon(opponent_score)
    new_score = score + gain
    if is_swap(new_score, opponent_score):
        if opponent_score > new_score:
            return 0
        else:
            return num_rolls
    else:
        if gain >= margin:
            return 0
        else:
            return num_rolls
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return swap_strategy(score, opponent_score)
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

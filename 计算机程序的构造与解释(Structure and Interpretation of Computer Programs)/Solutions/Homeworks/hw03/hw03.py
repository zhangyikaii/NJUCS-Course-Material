""" Homework 3: Recursion and Tree Recursion"""

HW_SOURCE_FILE = 'hw03.py'

#####################
# Required Problems #
#####################

def num_sevens(x):
    """Returns the number of times 7 appears as a digit of x.

    >>> num_sevens(3)
    0
    >>> num_sevens(7)
    1
    >>> num_sevens(7777777)
    7
    >>> num_sevens(2637)
    1
    >>> num_sevens(76370)
    2
    >>> num_sevens(12345)
    0
    >>> from construct_check import check
    >>> # ban all assignment statements
    >>> check(HW_SOURCE_FILE, 'num_sevens',
    ...       ['Assign', 'AugAssign'])
    True
    """
    assert x >= 0, 'Invalid Input'
    if x == 0:
        return 0
    if x % 10 == 7:
        return num_sevens(x // 10) + 1
    return num_sevens(x // 10)


def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> # ban assignment statements
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    # 'iter' is the abbreviation for 'iteration'.
    def iter(val, i, direction, stop): 
        if i > stop:
            return val
        if i % 7 == 0 or num_sevens(i) > 0:
            return iter(val + direction, i + 1, -direction, stop)
        return iter(val + direction, i + 1, direction, stop)
    return iter(0, 1, 1, n)


# Solution 2: 对n由大到小递归
# recursive_pingpong(n, direction)中的 direction 定义为 pingpong(n+1) - pingpong(n)，即下一次增减的方向
def pingpong2(n):
    def recursive_pingpong(m, direction):
        if m < 7:
            return m
        if m % 7 == 0 or num_sevens(m) > 0:
            return recursive_pingpong(m - 1, -direction) - direction
        return recursive_pingpong(m - 1, direction) + direction

    def calc_direction(m):
        if m < 7:
            return 1
        if m % 7 == 0 or num_sevens(m) > 0:
            return -calc_direction(m - 1)
        return calc_direction(m - 1)

    return recursive_pingpong(n, calc_direction(n))


def count_change(total):
    """Return the number of ways to make change for total.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_change', ['While', 'For'])
    True
    """
    def count_r(total, least_coin):
        if total == 0:
            return 1
        if least_coin > total:
            return 0
        return count_r(total - least_coin, least_coin) + count_r(total, least_coin * 2)
    return count_r(total, 1)


def missing_digits(n):
    """Given a number a that is in sorted, increasing order,
    return the number of missing digits in n. A missing digit is
    a number between the first and last digit of a that is not in n.
    >>> missing_digits(1248) # 3, 5, 6, 7
    4
    >>> missing_digits(1122) # No missing numbers
    0
    >>> missing_digits(123456) # No missing numbers
    0
    >>> missing_digits(3558) # 4, 6, 7
    3
    >>> missing_digits(4) # No missing numbers between 4 and 4
    0
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'missing_digits', ['While', 'For'])
    True
    """
    if n < 10:
        return 0
    right_first_digit = n % 10
    right_second_digit = (n // 10) % 10
    if right_second_digit < right_first_digit:
        return missing_digits(n // 10) + (right_first_digit - right_second_digit) - 1
    return missing_digits(n // 10)

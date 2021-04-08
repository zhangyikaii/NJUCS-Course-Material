""" Homework 2: Higher Order Functions"""

HW_SOURCE_FILE = 'hw02.py'

from operator import add, mul, sub

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


#####################
# Required Problems #
#####################
def compose(h, g):
    """Return a function f, such that f(x) = h(g(x)).

    >>> compose(square, triple)(5)
    225
    >>> double_inc = compose(increment, increment)
    >>> double_inc(3)
    5
    >>> double_inc(4)
    6
    """
    return lambda x: h(g(x))


def product(n, f):
    """Return the product of the first n terms in a sequence.
    n -- a positive integer
    f -- a function that takes one argument to produce the term

    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    Mproduct = 1
    while n > 0:
        Mproduct *= f(n)
        n -= 1
    return Mproduct


def accumulate(combiner, base, n, f):
    """Return the result of combining the first n terms in a sequence and base.
    The terms to be combined are f(1), f(2), ..., f(n).  combiner is a
    two-argument commutative, associative function.

    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19
    >>> accumulate(lambda x, y: 2 * (x + y), 2, 3, square)
    58
    >>> accumulate(lambda x, y: (x + y) % 17, 19, 20, square)
    16
    """
    if n == 0:
        return base
    i = 1
    while i <= n:
        base = combiner(base, f(i))
        i += 1
    return base


def summation_using_accumulate(n, f):
    """Returns the sum of f(1) + ... + f(n). The implementation
    uses accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'summation_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    return accumulate(add, 0, n, f)


def product_using_accumulate(n, f):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'product_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    return accumulate(mul, 1, n, f)


def make_repeater(h, n):
    """Return the function that computes the nth application of h.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times! 
    5
    """
    return int_to_church(n)(h)

    """def repeater(num):
        for i in range(n):
            num = h(num)
        return num
    return repeater"""

    """def repeater(i, time=n):
        return h(repeater(i, time-1)) if time else i
    return repeater"""


##########################
# Just for fun Questions #
##########################

def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: lambda x: f(n(f)(x))


def one(f):
    """Church numeral 1: same as successor(zero)"""
    return lambda x: f(x)


def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    return lambda x: f(f(x))


three = successor(two)


def pair(a, b):
    return lambda s: s(a, b)


def fst(a, b):
    return a


def sec(a, b):
    return b

def trans(p):
    return pair(p(sec), successor(p(sec)))

def pred(m, begin = pair(zero, zero)):
    if church_to_int(begin(sec)) == church_to_int(m):
        return begin(fst)
    return pred(m, trans(begin))

def int_to_church(n):
    """Convert a Python integer n to a Church numeral n.

    >>> church_to_int(int_to_church(5)) 
    5
    >>> church_to_int(add_church(int_to_church(49),int_to_church(51)))
    100
    """
    return successor(int_to_church(n - 1)) if n else zero


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    return n(lambda x: x + 1)(0)

def sub_church(m, n):
    """Return the Church numeral for m - n, for Church numerals m and n.
    >>> church_to_int(sub_church(int_to_church(20), int_to_church(20)))
    0
    >>> church_to_int(sub_church(int_to_church(2), int_to_church(0)))
    2
    >>> church_to_int(sub_church(int_to_church(600),int_to_church(0)))
    600
    """
    assert church_to_int(m) >= church_to_int(n),'There is no negative number in church numeral.'
    a = pair(m, n)
    return a(fst) if n is zero else sub_church(pred(m), pred(n))

def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    return lambda f: lambda x: m(f)(n(f)(x))


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    return lambda f: m(n(f))


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    return n(m)


l_true = lambda x: lambda y: x
l_false = lambda x: lambda y: y
l_not = lambda b: lambda x: lambda y: b(y)(x)


def church_to_bool(b):
    return b(True)(False)

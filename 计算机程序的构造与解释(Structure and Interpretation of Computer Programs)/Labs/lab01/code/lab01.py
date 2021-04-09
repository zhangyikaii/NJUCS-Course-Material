""" Lab 1: Variables & Functions, Control """

def both_positive(a, b):
    """Returns True if both a and b are positive.

    >>> both_positive(-1, 1)
    False
    >>> both_positive(1, 1)
    True
    """
    return a and b > 0 # You can replace this line!

def factorial(n):
    """Return the factorial of a positive integer n.

    >>> factorial(3)
    6
    >>> factorial(5)
    120
    """
    "*** YOUR CODE HERE ***"

def is_triangle(a, b, c):
    """Given three integers (may be nonpositive), judge whether the three
    integers can form the three sides of a triangle. If yes, return 1, 
    otherwise return 0.

    >>> is_triangle(2, 1, 3)
    0
    >>> is_triangle(5, -3, 4)
    0
    >>> is_triangle(2, 2, 2)
    1
    """
    "*** YOUR CODE HERE ***"

def number_of_two(n):
    """Return the number of 2 in each digit of a positive integer n.

    >>> number_of_two(123)
    1
    >>> number_of_two(2223)
    3
    """
    "*** YOUR CODE HERE ***"

def sum_digits(x):
    """Sum all the digits of x.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123) # make sure that you are using return rather than print
    >>> a
    6
    """
    "*** YOUR CODE HERE ***"
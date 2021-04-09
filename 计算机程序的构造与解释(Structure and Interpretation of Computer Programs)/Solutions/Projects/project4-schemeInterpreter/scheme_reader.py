"""This module implements the built-in data types of the Scheme language, along
with a parser for Scheme expressions.

In addition to the types defined in this file, some data types in Scheme are
represented by their corresponding type in Python:
    number:       int or float
    symbol:       string
    boolean:      bool
    unspecified:  None

The __repr__ method of a Scheme value will return a Python expression that
would be evaluated to the value, where possible.

The __str__ method of a Scheme value will return a Scheme expression that
would be read to the value, where possible.
"""

from __future__ import print_function  # Python 2 compatibility

import numbers

from ucb import main, trace, interact
from scheme_tokens import tokenize_lines, DELIMITERS
from buffer import Buffer, InputReader, LineReader


# Pairs and Scheme lists

class Pair(object):
    """A pair has two instance attributes: first and rest. rest must be a Pair or nil

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first, rest):
        from scheme_builtins import scheme_valid_cdrp, SchemeError
        if not (rest is nil or isinstance(rest, Pair) or type(rest).__name__ == 'Promise'):
            print(rest, type(rest).__name__)
            raise SchemeError("cdr can only be a pair, nil, or a promise but was {}".format(rest))
        self.first = first
        self.rest = rest

    def __repr__(self):
        return 'Pair({0}, {1})'.format(repr(self.first), repr(self.rest))

    def __str__(self):
        s = '(' + repl_str(self.first)
        rest = self.rest
        while isinstance(rest, Pair):
            s += ' ' + repl_str(rest.first)
            rest = rest.rest
        if rest is not nil:
            s += ' . ' + repl_str(rest)
        return s + ')'

    def __len__(self):
        n, rest = 1, self.rest
        while isinstance(rest, Pair):
            n += 1
            rest = rest.rest
        if rest is not nil:
            raise TypeError('length attempted on improper list')
        return n

    def __eq__(self, p):
        if not isinstance(p, Pair):
            return False
        return self.first == p.first and self.rest == p.rest

    def map(self, fn):
        """Return a Scheme list after mapping Python function FN to SELF."""
        mapped = fn(self.first)
        if self.rest is nil or isinstance(self.rest, Pair):
            return Pair(mapped, self.rest.map(fn))
        else:
            raise TypeError('ill-formed list (cdr is a promise)')

    def flatmap(self, fn):
        """Return a Scheme list after flatmapping Python function FN to SELF."""
        from scheme_builtins import scheme_append
        mapped = fn(self.first)
        if self.rest is nil or isinstance(self.rest, Pair):
            return scheme_append(mapped, self.rest.flatmap(fn))
        else:
            raise TypeError('ill-formed list (cdr is a promise)')


class nil(object):
    """The empty list"""

    def __repr__(self):
        return 'nil'

    def __str__(self):
        return '()'

    def __len__(self):
        return 0

    def map(self, fn):
        return self

    def flatmap(self, fn):
        return self

nil = nil() # Assignment hides the nil class; there is only one instance

# Scheme list parser



def scheme_read(src):
    """Read the next expression from SRC, a Buffer of tokens.

    >>> scheme_read(Buffer(tokenize_lines(['nil'])))
    nil
    >>> scheme_read(Buffer(tokenize_lines(['1'])))
    1
    >>> scheme_read(Buffer(tokenize_lines(['true'])))
    True
    >>> scheme_read(Buffer(tokenize_lines(['(+ 1 2)'])))
    Pair('+', Pair(1, Pair(2, nil)))
    """
    if src.current() is None:
        raise EOFError
    val = src.pop_first() # Get and remove the first token
    if val == 'nil':
        # BEGIN PROBLEM 1
        return nil
        # END PROBLEM 1
    elif val == '(':
        # BEGIN PROBLEM 1
        return read_tail(src)
        # END PROBLEM 1
    elif val == "'":
        # BEGIN PROBLEM 6
        return Pair('quote',Pair(scheme_read(src), nil))
        # END PROBLEM 6
    elif val not in DELIMITERS:
        return val
    else:
        raise SyntaxError('unexpected token: {0}'.format(val))
def read_tail(src):
    """Return the remainder of a list in SRC, starting before an element or ).

    >>> read_tail(Buffer(tokenize_lines([')'])))
    nil
    >>> read_tail(Buffer(tokenize_lines(['2 3)'])))
    Pair(2, Pair(3, nil))
    """
    try:
        if src.current() is None:
            raise SyntaxError('unexpected end of file')
        elif src.current() == ')':
            # BEGIN PROBLEM 1
            src.pop_first()
            return nil
            # END PROBLEM 1
        else:
            # BEGIN PROBLEM 1
            first = scheme_read(src)
            rest = read_tail(src)
            return Pair(first, rest)
            # END PROBLEM 1
    except EOFError:
        raise SyntaxError('unexpected end of file')

# Convenience methods

def buffer_input(prompt='scm> '):
    """Return a Buffer instance containing interactive input."""
    return Buffer(tokenize_lines(InputReader(prompt)))

def buffer_lines(lines, prompt='scm> ', show_prompt=False):
    """Return a Buffer instance iterating through LINES."""
    if show_prompt:
        input_lines = lines
    else:
        input_lines = LineReader(lines, prompt)
    return Buffer(tokenize_lines(input_lines))

def read_line(line):
    """Read a single string LINE as a Scheme expression."""
    buf = Buffer(tokenize_lines([line]))
    result = scheme_read(buf)
    if buf.more_on_line:
        raise SyntaxError("read_line's argument can only be a single element, but received multiple")
    return result

def repl_str(val):
    """Should largely match str(val), except for booleans and undefined."""
    if val is True:
        return "#t"
    if val is False:
        return "#f"
    if val is None:
        return "undefined"
    if isinstance(val, numbers.Number) and not isinstance(val, numbers.Integral):
        return repr(val)  # Python 2 compatibility
    return str(val)

# Interactive loop
def read_print_loop():
    """Run a read-print loop for Scheme expressions."""
    while True:
        try:
            src = buffer_input('read> ')
            while src.more_on_line:
                expression = scheme_read(src)
                if expression == 'exit':
                    print()
                    return
                print('str :', expression)
                print('repr:', repr(expression))
        except (SyntaxError, ValueError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            print()
            return

@main
def main(*args):
    if len(args) and '--repl' in args:
        read_print_loop()
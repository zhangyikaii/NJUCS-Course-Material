import string

from buffer import Buffer
from expr import *

SYMBOL_STARTS = set(string.ascii_lowercase + string.ascii_uppercase + '_')
SYMBOL_INNERS = SYMBOL_STARTS | set(string.digits)
NUMERAL = set(string.digits + '-.')
WHITESPACE = set(' \t\n\r')
DELIMITERS = set('(),:')

def read(s):
    """Parse an expression from a string. If the string does not contain an
    expression, None is returned. If the string cannot be parsed, a SyntaxError
    is raised.

    >>> read('lambda f: f(0)')
    LambdaExpr(['f'], CallExpr(Name('f'), [Literal(0)]))
    >>> read('(lambda x: x)(5)')
    CallExpr(LambdaExpr(['x'], Name('x')), [Literal(5)])
    >>> read('(lambda: 5)()')
    CallExpr(LambdaExpr([], Literal(5)), [])
    >>> read('lambda x y: 10')
    Traceback (most recent call last):
      ...
    SyntaxError: expected ':' but got 'y'
    >>> read('  ')  # returns None
    """
    src = Buffer(tokenize(s))
    if src.current() is not None:
        return read_expr(src)

###########
## Lexer ##
###########
def tokenize(s):
    """Splits the string s into tokens and returns a list of them.

    >>> tokenize('lambda f: f(0, 4.2)')
    ['lambda', 'f', ':', 'f', '(', 0, ',', 4.2, ')']
    """
    src = Buffer(s)
    tokens = []
    while True:
        token = next_token(src)
        if token is None:
            return tokens
        tokens.append(token)

def take(src, allowed_characters):
    result = ''
    while src.current() in allowed_characters:
        result += src.pop_first()
    return result

def next_token(src):
    take(src, WHITESPACE)  # skip whitespace
    c = src.current()
    if c is None:
        return None
    elif c in NUMERAL:
        literal = take(src, NUMERAL)
        try:
            return int(literal)
        except ValueError:
            try:
                return float(literal)
            except ValueError:
                raise SyntaxError("'{}' is not a numeral".format(literal))
    elif c in SYMBOL_STARTS:
        return take(src, SYMBOL_INNERS)
    elif c in DELIMITERS:
        src.pop_first()
        return c
    else:
        raise SyntaxError("'{}' is not a token".format(c))

def is_literal(s):
    return isinstance(s, int) or isinstance(s, float)

def is_name(s):
    return isinstance(s, str) and s not in DELIMITERS and s != 'lambda'

############
## Parser ##
############
def read_expr(src):
    token = src.pop_first()
    if token is None:
        raise SyntaxError('Incomplete expression')
    elif is_literal(token):
        return read_call_expr(src, Literal(token))
    elif is_name(token):
        return read_call_expr(src, Name(token))
    elif token == 'lambda':
        params = read_comma_separated(src, read_param)
        src.expect(':')
        body = read_expr(src)
        return LambdaExpr(params, body)
    elif token == '(':
        inner_expr = read_expr(src)
        src.expect(')')
        return read_call_expr(src, inner_expr)
    else:
        raise SyntaxError("'{}' is not the start of an expression".format(token))

def read_comma_separated(src, reader):
    if src.current() in (':', ')'):
        return []
    else:
        s = [reader(src)]
        while src.current() == ',':
            src.pop_first()
            s.append(reader(src))
        return s

def read_call_expr(src, operator):
    while src.current() == '(':
        src.pop_first()
        operands = read_comma_separated(src, read_expr)
        src.expect(')')
        operator = CallExpr(operator, operands)
    return operator

def read_param(src):
    token = src.pop_first()
    if is_name(token):
        return token
    else:
        raise SyntaxError("Expected parameter name but got '{}'".format(token))
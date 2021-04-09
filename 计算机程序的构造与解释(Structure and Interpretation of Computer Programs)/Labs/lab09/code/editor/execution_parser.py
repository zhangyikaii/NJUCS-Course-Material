from typing import Union

from datamodel import Expression, Symbol, Number, Nil, SingletonTrue, SingletonFalse, String
from helper import make_list
from lexer import TokenBuffer, SPECIALS
from log import logger
from scheme_exceptions import ParseError


def strip_comments(code):
    try:
        out = ""
        for string in code:
            if not string.strip():
                continue
            buff = TokenBuffer([string])
            while not buff.done:
                out += str(get_expression(buff))
        return out
    except ParseError:
        return str(code)


def tokenize(buffer: TokenBuffer):
    """
    >>> buff = TokenBuffer(["(1 (2 cat) (cat+dog-2 (5 6)  ) )"])
    >>> tokenize(buff)
    [(1 (2 cat) (cat+dog-2 (5 6)))]
    >>> buff = TokenBuffer(["(1 . 2)"])
    >>> tokenize(buff)
    [(1 . 2)]
    >>> buff = TokenBuffer(["(1 2 . 3)"])
    >>> tokenize(buff)
    [(1 2 . 3)]
    >>> buff = TokenBuffer(["1"])
    >>> tokenize(buff)
    [1]
    """
    out = []  # array of top-level elements to be executed sequentially
    while not buffer.done:
        out.append(get_expression(buffer))
        if out[-1] is None:
            out.pop()
    return out


def get_expression(buffer: TokenBuffer) -> Union[Expression, None]:
    token = buffer.pop_next_token()
    if token is None:
        return None
    elif token in ("(", "["):
        return get_rest_of_list(buffer, ")" if token == "(" else "]")
    elif token == "'":
        return make_list([Symbol("quote"), get_expression(buffer)])
    elif token == ",":
        if buffer.get_next_token() == "@":
            buffer.pop_next_token()
            return make_list([Symbol("unquote-splicing"), get_expression(buffer)])
        else:
            return make_list([Symbol("unquote"), get_expression(buffer)])
    elif token == "`":
        return make_list([Symbol("quasiquote"), get_expression(buffer)])
    elif token == ".":
        if logger.dotted:
            raise ParseError(f"Unexpected token: '{token}'")
        else:
            return make_list([Symbol("variadic"), get_expression(buffer)])
    elif token == "\"":
        return get_string(buffer)
    elif token in SPECIALS:
        raise ParseError(f"Unexpected token: '{token}'")
    elif is_number(token.value):
        try:
            return Number(int(token.value))
        except ValueError:
            return Number(float(token.value))
    elif token == "#t" or token.value.lower() == "true":
        return SingletonTrue
    elif token == "#f" or token.value.lower() == "false":
        return SingletonFalse
    elif token == "nil":
        return Nil
    elif is_str(token.value):
        return Symbol(token.value.lower())
    else:
        raise ParseError(f"Unexpected token: '{token}'")


def get_string(buffer: TokenBuffer) -> String:
    out = []
    string = buffer.pop_next_token()
    escaping = False
    for char in string.value:
        if escaping:
            if char == "n":
                out.append("\n")
            else:
                out.append(char)
            escaping = False
        elif char == "\\":
            escaping = True
        else:
            out.append(char)
    if buffer.pop_next_token() != "\"":
        raise ParseError("String not terminated correctly!")
    return String("".join(out))


def get_rest_of_list(buffer: TokenBuffer, end_paren: str) -> Expression:
    out = []
    last = Nil
    while True:
        next = buffer.get_next_token()
        if next == end_paren:
            buffer.pop_next_token()
            break
        elif logger.dotted and next == ".":
            buffer.pop_next_token()
            last = get_expression(buffer)
            if buffer.pop_next_token() != end_paren:
                raise ParseError(f"Only one expression may follow a dot in a dotted list.")
            break
        expr = get_expression(buffer)
        out.append(expr)
    out = make_list(out, last)
    return out


def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


def is_str(token: str) -> bool:
    return True

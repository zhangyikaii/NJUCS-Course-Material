from typing import Union, List

from lexer import TokenBuffer, SPECIALS, Comment
from scheme_exceptions import ParseError


class FormatList:
    def __init__(self,
                 contents: List['Formatted'],
                 close_paren,
                 prefix: str=""):
        self.contents = contents
        self.open_paren = "(" if close_paren == ")" else "["
        self.close_paren = close_paren
        self.prefix = prefix

    class PrefixManager:
        def __init__(self, lst):
            self.lst = lst

        def __enter__(self):
            self.prefix = self.lst.prefix[0]
            self.lst.prefix = self.lst.prefix[1:]
            return self.prefix

        def __exit__(self, *_):
            self.lst.prefix = self.prefix + self.lst.prefix

    def hold_prefix(self):
        return self.PrefixManager(self)


class FormatAtom:
    def __init__(self, value: str):
        self.value = value
        self.prefix = ""


class FormatComment:
    def __init__(self, value: str, allow_inline: bool):
        self.value = value
        self.prefix = ""
        self.allow_inline = allow_inline


Formatted = Union[FormatList, FormatAtom, FormatComment]


def get_expression(buffer: TokenBuffer) -> Formatted:
    token = buffer.pop_next_token()
    if isinstance(token, Comment):
        return FormatComment(token.value, not token.first_in_line)
    elif token == "#" and not buffer.done and buffer.get_next_token() == "[":
        buffer.pop_next_token()
        out = FormatAtom("#[" + buffer.pop_next_token().value + "]")
        buffer.pop_next_token()
    elif token in SPECIALS:
        if token in ("(", "["):
            out = get_rest_of_list(buffer, ")" if token == "(" else "]")
        elif token in ("'", "`"):
            out = get_expression(buffer)
            out.prefix = token.value + out.prefix
        elif token == ",":
            if buffer.get_next_token() == "@":
                buffer.pop_next_token()
                out = get_expression(buffer)
                out.prefix = ",@" + out.prefix
            else:
                out = get_expression(buffer)
                out.prefix = token.value + out.prefix
        elif token == "\"":
            out = FormatAtom('"' + buffer.pop_next_token().value + '"')
            buffer.pop_next_token()
        else:
            raise ParseError(f"Unexpected token: '{token}'")

    else:
        if token.value.lower() == "true":
            token.value = "#t"
        elif token.value.lower() == "false":
            token.value = "#f"
        out = FormatAtom(token.value)

    return out


def get_rest_of_list(buffer: TokenBuffer, end_paren: str):
    out = []
    while buffer.get_next_token() != end_paren:
        out.append(get_expression(buffer))
    buffer.pop_next_token()
    return FormatList(out, end_paren)

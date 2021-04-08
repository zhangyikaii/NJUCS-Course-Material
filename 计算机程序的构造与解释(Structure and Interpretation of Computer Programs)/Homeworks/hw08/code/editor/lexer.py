from typing import Union, List

from scheme_exceptions import ParseError

SPECIALS = ["(", ")", "[", "]", "'", "`", ",", "@", "\"", ";"]


class Token:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        return other == self.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Comment(Token):
    def __init__(self, value: str, first_in_line: bool):
        super().__init__(value)
        self.first_in_line = first_in_line


class TokenBuffer:
    def __init__(self, lines, do_comments=False, ignore_brackets=False):
        self.string = "\n".join(lines)
        self.tokens = tokenize(self.string, do_comments, ignore_brackets)
        self.done = not self.tokens
        self.i = 0

    def get_next_token(self) -> Token:
        if self.done:
            raise ParseError("Incomplete expression, probably due to unmatched parentheses.")
        return self.tokens[self.i]

    def pop_next_token(self) -> Token:
        out = self.get_next_token()
        self.i += 1
        if self.i == len(self.tokens):
            self.done = True
        return out


def tokenize(string, do_comments, ignore_brackets) -> List[Token]:
    string = string.strip()
    tokens = []
    i = 0
    first_in_line = True

    def _get_token():
        """Always starts at a non-space character"""
        nonlocal i
        if i == len(string):
            return
        if string[i] == "\"":
            tokens.append(Token(string[i]))
            i += 1
            _get_string()
            return

        elif string[i] == ";":
            i += 1
            _get_comment()

        elif string[i] in SPECIALS and not (ignore_brackets and string[i] in ["[", "]"]):
            tokens.append(Token(string[i]))
            i += 1

        else:
            curr = ""
            while i != len(string) and not string[i].isspace() and string[i] not in SPECIALS:
                curr += string[i]
                i += 1
            if curr:
                tokens.append(Token(curr))

    def _get_comment():
        nonlocal i
        curr = ""
        while i != len(string) and string[i] != "\n":
            curr += string[i]
            i += 1
        if do_comments:
            tokens.append(Comment(curr, first_in_line))

    def _get_string():
        """Starts just after an opening quotation mark"""
        nonlocal i
        curr = ""
        while i != len(string) and string[i] != "\"":
            char = string[i]
            if char == "\n":
                raise ParseError("Multiline strings not supported!")
            if char == "\\":
                curr += char
                if i + 1 == len(string):
                    raise ParseError("String not terminated correctly (try escaping the backslash?)")
                curr += string[i + 1]
                i += 2
            else:
                curr += string[i]
                i += 1
        tokens.append(Token(curr))
        if i == len(string):
            raise ParseError("String missing a closing quote")
        tokens.append(Token(string[i]))
        i += 1

    while i != len(string):
        _get_token()
        first_in_line = False
        while i != len(string) and string[i].isspace():
            if string[i] == "\n":
                first_in_line = True
            i += 1

    return tokens

from abc import ABC
from functools import lru_cache
from typing import List, Tuple, Type, Union

import lexer as lexer
from format_parser import FormatAtom, FormatComment, FormatList, Formatted, get_expression

LINE_LENGTH = 50
MAX_EXPR_COUNT = 10
MAX_EXPR_LEN = 30
INDENT = 4

DEFINE_VALS = ["define", "define-macro"]
DECLARE_VALS = ["lambda", "mu"]
SHORTHAND = {"quote": "'", "quasiquote": "`", "unquote": ",", "unquote-splicing": ",@", "variadic": "."}
MULTILINE_VALS = ["let", "cond", "if"]

FREE_TOKENS = ["if", "define", "define-macro", "mu", "lambda"]

OPEN_PARENS = ["(", "["]
CLOSE_PARENS = [")", "]"]

CACHE_SIZE = 2 ** 8


def prettify(strings: List[str], javastyle: bool = False) -> str:
    out = []
    for i, string in enumerate(strings):
        if not string.strip():
            continue
        out.extend(prettify_single(string, javastyle))

    raw_out = []
    for expr in out:
        if expr.startswith(";"):
            raw_out.append(expr)
        else:
            raw_out.append(expr)
            raw_out.append("\n")
        raw_out.append("\n")

    while raw_out and raw_out[-1] == "\n":
        raw_out.pop()

    return "".join(raw_out)


@lru_cache(CACHE_SIZE)
def prettify_single(string: str, javastyle: bool) -> List[str]:
    Formatter.set_javastyle(javastyle)
    out = []
    buff = lexer.TokenBuffer([string], True)
    while not buff.done:
        expr = get_expression(buff)
        out.append(ExpressionFormatter.format(expr, LINE_LENGTH).stringify())
    return out


class OptimalFormattingReached(Exception):
    pass


class MatchFailure(Exception):
    pass


class WeakMatchFailure(MatchFailure):
    pass


class StrongMatchFailure(MatchFailure):
    ...


class FormatSeq:
    def __init__(self):
        self.left: FormatOp = None
        self.right: FormatOp = None
        self.active = True
        self.line_lengths = [0]
        self.max_line_len = 0
        self.cost = 0

    def __add__(self, other):
        if other is None:
            return self
        if isinstance(other, FormatSeq):
            return other.__radd__(self)
        return NotImplemented

    def __radd__(self, other: 'FormatSeq'):
        if other is None:
            return self
        if not other.active:
            raise Exception("Attempting to manipulate inactive seqs!")
        if not self.active:
            raise Exception("???")
        other.right.next = self.left
        other.active = False
        self.left = other.left
        self.line_lengths[0] += other.line_lengths.pop()
        self.line_lengths = other.line_lengths + self.line_lengths
        self.max_line_len = max(self.max_line_len, other.max_line_len, *self.line_lengths)
        if len(self.line_lengths) > 1:
            self.line_lengths = [self.line_lengths[0], self.line_lengths[-1]]
        return self

    def contains_newline(self):
        return len(self.line_lengths) > 1

    def stringify(self):
        pos = self.left
        out = []
        indent_level = 0
        while pos is not None:
            if isinstance(pos, _Token):
                out.append(pos.value)
                if pos.value == "\n":
                    out.append(" " * indent_level)
            elif isinstance(pos, _ChangeIndent):
                indent_level += pos.level
            else:
                raise NotImplementedError("unable to stringify " + str(type(pos)))
            pos = pos.next
        return "".join(out)


class FormatOp:
    def __init__(self):
        self.next = None


class _Token(FormatOp):
    def __init__(self, value):
        super().__init__()
        assert isinstance(value, str)
        self.value = value


class Token(FormatSeq):
    def __init__(self, value):
        super().__init__()
        self.left = self.right = _Token(value)
        self.max_line_len = self.line_lengths[0] = len(value)


class _ChangeIndent(FormatOp):
    def __init__(self, level):
        super().__init__()
        self.level = level


class ChangeIndent(FormatSeq):
    def __init__(self, level):
        super().__init__()
        self.left = self.right = _ChangeIndent(level)


class Newline(Token):
    def __init__(self):
        super().__init__("\n")
        self.max_line_len = self.line_lengths[0] = 0
        self.line_lengths.append(0)


class Space(Token):
    def __init__(self):
        super().__init__(" ")


class Formatter(ABC):
    javastyle = False

    @staticmethod
    def format(expr: Formatted, remaining: int) -> FormatSeq:
        raise NotImplementedError()

    @staticmethod
    def set_javastyle(javastyle: bool):
        Formatter.javastyle = javastyle


class SpecialFormFormatter(Formatter, ABC):
    @classmethod
    def assert_form(cls, expr: Formatted, form: Union[str, List[str]]):
        if isinstance(form, list):
            for elem in form:
                try:
                    cls.assert_form(expr, elem)
                except WeakMatchFailure:
                    continue
                else:
                    return
            raise WeakMatchFailure

        if not isinstance(expr, FormatList):
            raise WeakMatchFailure("Special form must be list, not atom.")
        if not expr.contents:
            raise WeakMatchFailure("Special form must be list, not nil.")
        if not isinstance(expr.contents[0], FormatAtom):
            raise WeakMatchFailure("Special form must begin with a Symbol.")
        if not expr.contents[0].value == form:
            raise WeakMatchFailure("Call expression does not match desired special form.")
        # if expr.last:
        #     raise StrongMatchFailure("Special form must not be dotted.")

    @classmethod
    def match_form(cls, expr: Formatted, form: Union[str, List[str]]):
        try:
            cls.assert_form(expr, form)
        except WeakMatchFailure:
            return False
        else:
            return True

    @classmethod
    def is_multiline(cls, expr: Formatted):
        return any(cls.match_form(expr, form) for form in MULTILINE_VALS)


class AlignedCondFormatter(SpecialFormFormatter):
    class Clause(Formatter):
        @staticmethod
        def format(expr: Formatted, remaining: int, max_pred_len: int = 0) -> FormatSeq:
            if isinstance(expr, FormatComment):
                return CommentFormatter.format(expr)
            else:
                out = Token(expr.prefix) + Token(expr.open_paren)
                inlined_pred = InlineFormatter.format(expr.contents[0])
                pred_len = len(expr.prefix) + inlined_pred.max_line_len
                out += inlined_pred
                out += Token(" " * (max_pred_len - pred_len)) + Space()
                out += InlineFormatter.format(expr.contents[1])
                out += Token(expr.close_paren)
                return out

        @staticmethod
        def pred_len(expr: Formatted):
            if isinstance(expr, FormatAtom):
                raise WeakMatchFailure("Cond clause should not be FormatAtom")
            elif isinstance(expr, FormatComment):
                return 0
            else:
                if len(expr.contents) != 2:
                    raise WeakMatchFailure("Cannot auto-align expr")
                pred, val = expr.contents
                inlined_pred = InlineFormatter.format(pred)
                return inlined_pred.max_line_len

    @classmethod
    def format(cls, expr: Formatted, remaining) -> FormatSeq:
        cls.assert_form(expr, "cond")
        max_pred_len = 0
        for clause in expr.contents[1:]:
            max_pred_len = max(max_pred_len, cls.Clause.pred_len(clause))

        out = Token(expr.open_paren) + Token("cond") + Space() + ChangeIndent(2) + Newline()

        out += rest_format(expr.contents[1:], -1, max_pred_len,
                           formatter=cls.Clause, indent_level=2, close_paren=expr.close_paren)

        return out


class MultilineCondFormatter(SpecialFormFormatter):
    class Clause(Formatter):
        @staticmethod
        def format(expr: Formatted, remaining: int) -> FormatSeq:
            if isinstance(expr, FormatList):
                return NoHangingListFormatter.format(expr, remaining)
            else:
                return ExpressionFormatter.format(expr, remaining)

    @classmethod
    def format(cls, expr: Formatted, remaining) -> FormatSeq:
        cls.assert_form(expr, "cond")

        out = Token(expr.open_paren) + Token("cond") + Space() + ChangeIndent(2) + Newline()

        out += rest_format(expr.contents[1:], remaining - 2,
                           formatter=cls.Clause, indent_level=2, close_paren=expr.close_paren)

        return out


class LetFormatter(SpecialFormFormatter):
    class LetHandler(Formatter):
        def __init__(self):
            self.bindings_next = True

        def format(self, expr: Formatted, remaining: int) -> FormatSeq:
            if isinstance(expr, FormatList) and self.bindings_next:
                self.bindings_next = False
                out = NoHangingListFormatter.format(expr, remaining)
                out += ChangeIndent(-3)
                return out
            else:
                return ExpressionFormatter.format(expr, remaining)

    @classmethod
    def format(cls, expr: Formatted, remaining: int) -> FormatSeq:
        cls.assert_form(expr, "let")
        out = Token(expr.open_paren) + Token("let") + Space() + ChangeIndent(5)

        let_handler = cls.LetHandler()
        out += rest_format(expr.contents[1:], remaining - 6,
                           formatter=let_handler, indent_level=2, close_paren=expr.close_paren)

        if let_handler.bindings_next:
            raise WeakMatchFailure("Let statement with too few arguments")

        return out


class ProcedureFormatter(SpecialFormFormatter):
    class ProcedureHandler(Formatter):
        def __init__(self, indent_level):
            self.formals_next = True
            self.indent_level = indent_level

        def format(self, expr: Formatted, remaining: int) -> FormatSeq:
            out = ExpressionFormatter.format(expr, remaining)
            if isinstance(expr, FormatList) and self.formals_next:
                self.formals_next = False
                out += ChangeIndent(2 - self.indent_level)
            return out

    @classmethod
    def format(cls, expr: Formatted, remaining: int) -> FormatSeq:
        cls.assert_form(expr, DEFINE_VALS + DECLARE_VALS)

        indent_level = 2 + len(expr.contents[0].value)
        out = Token(expr.open_paren) + Token(expr.contents[0].value) + Space() + ChangeIndent(indent_level)

        procedure_handler = cls.ProcedureHandler(indent_level)
        out += rest_format(expr.contents[1:], remaining - indent_level,
                           formatter=procedure_handler, indent_level=2, close_paren=expr.close_paren)

        if procedure_handler.formals_next:
            raise WeakMatchFailure("Formals not specified")

        return out


class AtomFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int = None) -> FormatSeq:
        if not isinstance(expr, FormatAtom):
            raise WeakMatchFailure("expr is not atomic")
        return Token(expr.prefix + expr.value)


class InlineFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int = None) -> FormatSeq:
        if isinstance(expr, FormatComment):
            raise WeakMatchFailure("Cannot inline-format a comment")
        if isinstance(expr, FormatAtom):
            return AtomFormatter.format(expr, remaining)
        if SpecialFormFormatter.is_multiline(expr):
            raise WeakMatchFailure("Cannot inline-format a multiline expr")

        formatted_exprs = [InlineFormatter.format(elem) for elem in expr.contents]

        out = Token(expr.prefix) + Token(expr.open_paren)
        for formatted_expr in formatted_exprs:
            out += formatted_expr
            if formatted_expr is not formatted_exprs[-1]:
                out += Space()
        out += Token(expr.close_paren)
        return out


class ListFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int) -> FormatSeq:
        if not isinstance(expr, FormatList):
            raise WeakMatchFailure("expr is not a list")
        return find_best(expr, [InlineFormatter, PrefixedListFormatter, CallExprFormatter, NoHangingListFormatter],
                         remaining)


class CallExprFormatter(Formatter):
    @staticmethod
    def format(expr: FormatList, remaining: int) -> FormatSeq:
        assert isinstance(expr, FormatList)
        if len(expr.contents) <= 1:
            raise WeakMatchFailure("Call expr must have at least 2 arguments, otherwise handle using DataListFormatter")
        if expr.prefix:
            raise WeakMatchFailure("Call expr cannot be prefixed")
        if not isinstance(expr.contents[0], FormatAtom):
            raise WeakMatchFailure("Unable to inline first two arguments, fallback to DataListFormatter")
        return find_best(expr, [
            AlignedCondFormatter,
            MultilineCondFormatter,
            LetFormatter,
            ProcedureFormatter,
            DefaultCallExprFormatter], remaining)


class PrefixedListFormatter(Formatter):
    @staticmethod
    def format(expr: FormatList, remaining: int):
        assert isinstance(expr, FormatList)
        if not expr.prefix:
            raise WeakMatchFailure("Expr is not prefixed")
        with expr.hold_prefix() as prefix:
            if prefix == "`":
                ret = ListFormatter.format(expr, remaining - 1)
            else:
                ret = DataFormatter.format(expr, remaining - 1)
        return Token(prefix) + ChangeIndent(1) + ret + ChangeIndent(-1)


class DefaultCallExprFormatter(Formatter):
    @staticmethod
    def format(expr: FormatList, remaining: int) -> FormatSeq:
        operator = expr.contents[0]

        assert isinstance(operator, FormatAtom)

        indent_level = len(operator.value) + 2
        out = Token(expr.open_paren)
        out += AtomFormatter.format(operator)
        out += ChangeIndent(indent_level) + Space()

        out += rest_format(expr.contents[1:], remaining - indent_level,
                           indent_level=indent_level, close_paren=expr.close_paren)

        return out


class DataFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int) -> FormatSeq:
        if isinstance(expr, FormatComment):
            return CommentFormatter.format(expr)
        elif isinstance(expr, FormatAtom):
            return AtomFormatter.format(expr)
        else:
            return NoHangingListFormatter.format(expr, remaining, DataFormatter)


class NoHangingListFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int, callback: Type[Formatter] = None) -> FormatSeq:
        if callback is None:
            callback = ExpressionFormatter
        if expr.prefix:
            raise WeakMatchFailure("Cannot format prefixed datalist")
        out = Token(expr.open_paren) + ChangeIndent(1)
        out += rest_format(expr.contents, remaining - 1,
                           formatter=callback, indent_level=1, close_paren=expr.close_paren)
        return out


class CommentFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int = None) -> FormatSeq:
        if not isinstance(expr, FormatComment):
            raise WeakMatchFailure("Expr is not a comment")
        leading_space = "" if expr.value.startswith(" ") else " "
        return Token(expr.prefix + ";" + leading_space + expr.value)


class ExpressionFormatter(Formatter):
    @staticmethod
    def format(expr: Formatted, remaining: int) -> FormatSeq:
        candidates = [AtomFormatter, ListFormatter, CommentFormatter]
        return find_best(expr, candidates, remaining)


class Best:
    def __init__(self, remaining):
        self.curr_best = None
        self.curr_cost = None
        self.remaining = remaining

    def heuristic(self, chain: FormatSeq) -> int:
        return max(0, chain.max_line_len - 50) + chain.cost

    def add(self, formatted: FormatSeq):
        cost = self.heuristic(formatted)
        if self.curr_cost is None or cost < self.curr_cost:
            self.curr_best = formatted
            self.curr_cost = cost
            if cost == 0:
                raise OptimalFormattingReached()

    def get_best(self) -> FormatSeq:
        assert self.curr_best is not None
        return self.curr_best


def find_best(raw: Formatted, candidates: List[Type[Formatter]], remaining) -> FormatSeq:
    best = Best(remaining)
    for candidate in candidates:
        try:
            best.add(candidate.format(raw, remaining))
        except WeakMatchFailure as e:
            continue
        except StrongMatchFailure:
            # TODO: Warn about potentially invalid special form
            continue
        except OptimalFormattingReached:
            return best.get_best()
    return best.get_best()


def rest_format(exprs: List[Formatted],
                *args,
                formatter: Union[Formatter, Type[Formatter]] = ExpressionFormatter,
                indent_level: int,
                close_paren: str) -> Tuple[FormatSeq, bool]:
    out = None
    i = 0

    while i != len(exprs):
        curr_expr = exprs[i]
        i += 1
        formatted_expr = formatter.format(curr_expr, *args)
        if "not formatted_expr.contains_newline()" and i != len(exprs) \
                and not isinstance(curr_expr, FormatComment) \
                and isinstance(exprs[i], FormatComment) \
                and exprs[i].allow_inline:
            inline_comment = exprs[i]
            formatted_expr += Space() + CommentFormatter.format(inline_comment)
            i += 1
        out += formatted_expr if i == len(exprs) else formatted_expr + Newline()
    ends_with_comment = exprs and isinstance(exprs[-1], FormatComment)

    out += ChangeIndent(-indent_level)
    if ends_with_comment or Formatter.javastyle:
        out += Newline()

    out += Token(close_paren)

    return out

from typing import TYPE_CHECKING

from log_utils import get_id
from scheme_exceptions import TypeMismatchError

if TYPE_CHECKING:
    from evaluate_apply import Frame
    from log import Heap


class Expression:
    def __init__(self):
        self.id = None


class ValueHolder(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return str(self.value)


class Symbol(ValueHolder):
    pass


class Number(ValueHolder):
    def __init__(self, value, *, force_float=False):
        super().__init__(value)
        if value == round(value) and not force_float:
            self.value = round(value)
        else:
            self.value = value

    def __repr__(self):
        return super().__repr__()



class Pair(Expression):
    def __init__(self, first: Expression, rest: Expression):
        import log
        super().__init__()
        self.first = first
        if not log.logger.dotted and not isinstance(rest, (Pair, NilType, Promise)):
            raise TypeMismatchError(
                f"Unable to construct a Pair with a cdr of {rest}, expected a Pair, Nil, or Promise.")
        self.rest = rest

    def __repr__(self):
        pos = self
        out = []
        while True:
            if isinstance(pos, Pair):
                out.append(repr(pos.first))
                pos = pos.rest
            elif isinstance(pos, NilType):
                break
            else:
                out.append(f". {repr(pos)}")
                break
        return "(" + " ".join(out) + ")"


class NilType(Expression):
    def __repr__(self):
        return "()"


class UndefinedType(Expression):
    def __repr__(self):
        from log import logger
        if logger.strict_mode:
            return ""
        return "undefined"


class Boolean(ValueHolder):
    def __repr__(self):
        if self.value:
            return "#t"
        else:
            return "#f"


class String(ValueHolder):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return "\"" + self.value.replace("\n", "\\n").replace("\"", "\\\"").replace("\'", "'") + "\""


class Promise(Expression):
    def __init__(self, expr: Expression, frame: 'Frame'):
        super().__init__()
        self.forced = False
        self.force_i = None
        self.expr = expr
        self.frame = frame
        self.targets = []
        self.id = get_id()

    def __repr__(self):
        return "#[promise]"

    def bind(self) -> 'Heap.HeapKey':
        import log
        if self.forced:
            target = ["promise", [self.force_i, log.logger.heap.record(self.expr)]]
        else:
            target = ["promise", [99999999999999, None]]
        self.targets.append(target)
        return target

    def force(self):
        import log
        self.forced = True
        self.force_i = log.logger.i
        for target in self.targets:
            target[:] = ["promise", [self.force_i, log.logger.heap.record(self.expr)]]
        log.logger.heap.modify(self.id)


SingletonTrue = Boolean(True)
SingletonFalse = Boolean(False)

bools = [SingletonFalse, SingletonTrue]

Nil = NilType()
Undefined = UndefinedType()

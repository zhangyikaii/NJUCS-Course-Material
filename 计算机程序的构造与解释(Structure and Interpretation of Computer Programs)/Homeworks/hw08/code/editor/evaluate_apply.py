from typing import Dict, List, Union, Optional

import log
from datamodel import Symbol, Expression, Number, Pair, Nil, Undefined, Boolean, String, Promise
from helper import pair_to_list
from scheme_exceptions import SymbolLookupError, CallableResolutionError, IrreversibleOperationError, OutOfMemoryError


RECURSION_LIMIT = 100000


class Frame:
    def __init__(self, name: str, parent: 'Frame' = None):
        self.parent = parent
        self.name = name
        self.vars: Dict[str, Expression] = {}
        self.id = "unknown"
        self.temp = log.logger.fragile
        log.logger.frame_create(self)

    def assign(self, varname: Symbol, varval: Expression):
        if log.logger.fragile and not self.temp:
            raise IrreversibleOperationError()
        if isinstance(varval, Thunk):
            assert varname == log.return_symbol
            varval.bind(self)
            return
        self.vars[varname.value] = varval
        log.logger.frame_store(self, varname.value, varval)

    def mutate(self, varname: Symbol, varval: Expression):
        if log.logger.fragile and not self.temp:
            raise IrreversibleOperationError()
        assert not isinstance(varval, Thunk)
        if varname.value in self.vars:
            self.vars[varname.value] = varval
            log.logger.frame_store(self, varname.value, varval)
        elif self.parent is None:
            raise SymbolLookupError(f"Variable not found in current environment: '{varname}'")
        else:
            self.parent.mutate(varname, varval)

    def lookup(self, varname: Symbol):
        if varname.value in self.vars:
            return self.vars[varname.value]
        if self.parent is None:
            raise SymbolLookupError(f"Variable not found in current environment: '{varname}'")
        return self.parent.lookup(varname)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return repr(self.vars)


class Thunk:
    def __init__(self, expr: Expression, frame: Frame, gui_holder: log.Holder, log_stack: bool):
        self.expr = expr
        self.frame = frame
        self.log_stack = log_stack
        self.gui_holder = gui_holder
        self.return_frame: Optional[Frame] = None

    def __repr__(self):
        return "thunk"

    def evaluate(self, expr: Expression):
        if self.return_frame is not None:
            self.return_frame.assign(log.return_symbol, expr)

    def bind(self, return_frame: Frame):
        self.return_frame = return_frame


def evaluate(expr: Expression, frame: Frame, gui_holder: log.Holder,
             tail_context: bool = False, *, log_stack: bool=True) -> Union[Expression, Thunk]:
    depth = 0
    thunks = []
    holders = []

    while True:
        if depth > RECURSION_LIMIT:
            raise OutOfMemoryError("Debugger ran out of memory due to excessively deep recursion.")

        visual_expression = gui_holder.expression

        if log_stack:
            log.logger.eval_stack.append(f"{repr(expr)} [frame = {frame.id}]")
            depth += 1

        holders.append(gui_holder)

        if isinstance(expr, Number) \
                or isinstance(expr, Callable) \
                or isinstance(expr, Boolean) \
                or isinstance(expr, String) \
                or isinstance(expr, Promise):
            ret = expr
        elif isinstance(expr, Symbol):
            gui_holder.evaluate()
            ret = frame.lookup(expr)
        elif isinstance(expr, Pair):
            if tail_context:
                if log_stack:
                    log.logger.eval_stack.pop()
                return Thunk(expr, frame, gui_holder, log_stack)
            else:
                gui_holder.evaluate()
                operator = expr.first
                import environment
                if isinstance(operator, Symbol) and environment.get_special_form(operator.value):
                    operator = environment.get_special_form(operator.value)
                else:
                    operator = evaluate(operator, frame, visual_expression.children[0])
                operands = pair_to_list(expr.rest)
                out = apply(operator, operands, frame, gui_holder)
                if isinstance(out, Thunk):
                    expr, frame = out.expr, out.frame
                    thunks.append(out)
                    if out.gui_holder.state != log.HolderState.EVALUATING:
                        out.gui_holder.evaluate()
                    if log.logger.show_thunks:
                        gui_holder = out.gui_holder
                    else:
                        gui_holder.expression.display_value = out.gui_holder.expression.display_value
                        gui_holder.expression.base_expr = out.gui_holder.expression.base_expr
                        gui_holder.expression.set_entries(list(x.expression for x in out.gui_holder.expression.children))
                    continue
                ret = out
        elif expr is Nil or expr is Undefined:
            ret = expr
        else:
            raise Exception("Internal error. Please report to maintainer!")

        for _ in range(depth):
            log.logger.eval_stack.pop()

        for thunk, holder in zip(reversed(thunks), reversed(holders)):
            holder.expression.value = ret
            holder.complete()
            thunk.evaluate(ret)

        holders[0].expression.value = ret
        holders[0].complete()

        return ret


def apply(operator: Expression, operands: List[Expression], frame: Frame, gui_holder: log.Holder):
    if isinstance(operator, Callable):
        return operator.execute(operands, frame, gui_holder)
    elif isinstance(operator, Symbol):
        raise CallableResolutionError(f"Unable to pass parameters into the Symbol '{operator}'")
    else:
        raise CallableResolutionError(f"Unable to pass parameters into: '{operator}'")


class Callable(Expression):
    def execute(self, operands: List[Expression], frame: Frame, gui_holder: log.Holder):
        raise NotImplementedError()


class Applicable(Callable):
    def execute(self, operands: List[Expression], frame: Frame, gui_holder: log.Holder, eval_operands=True):
        raise NotImplementedError()


def evaluate_all(operands: List[Expression], frame: Frame, operand_holders: List[log.Holder]) -> List[Expression]:
    return [evaluate(operand, frame, holder) for operand, holder in zip(operands, operand_holders)]

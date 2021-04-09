import json
from typing import List

import log
from datamodel import Expression, Undefined, Pair
from environment import global_attr
from evaluate_apply import Frame
from helper import verify_exact_callable_length
from primitives import BuiltIn, SingleOperandPrimitive
from scheme_exceptions import IrreversibleOperationError, OperandDeduceError


@global_attr("autodraw")
class AutoDraw(BuiltIn):
        def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
            verify_exact_callable_length(self, 0, len(operands))
            if log.logger.fragile:
                raise IrreversibleOperationError()
            log.logger.raw_out("Disable autodraw with (disable-autodraw).\n")
            log.logger.raw_out("ENABLE_AUTODRAW[]\n")
            return Undefined


@global_attr("disable-autodraw")
class DisableAutoDraw(BuiltIn):
        def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
            verify_exact_callable_length(self, 0, len(operands))
            if log.logger.fragile:
                raise IrreversibleOperationError()
            log.logger.raw_out("DISABLE_AUTODRAW[]\n")
            return Undefined


@global_attr("draw")
class Draw(SingleOperandPrimitive):
        def execute_simple(self, operand: Expression) -> Expression:
            if log.logger.fragile:
                raise IrreversibleOperationError()
            log.logger.raw_out("DRAW" +
                               json.dumps([log.logger.i, log.logger.heap.record(operand)]) + "\n")
            return Undefined

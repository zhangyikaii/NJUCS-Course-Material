from typing import List

from datamodel import Expression, Number, bools, SingletonFalse, ValueHolder, Pair, SingletonTrue
from environment import global_attr
from evaluate_apply import Frame
from helper import assert_all_numbers, verify_exact_callable_length, verify_min_callable_length
from primitives import BuiltIn, SingleOperandPrimitive


@global_attr("+")
class Add(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame):
        assert_all_numbers(operands)
        return Number(sum(operand.value for operand in operands))


@global_attr("-")
class Subtract(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame):
        verify_min_callable_length(self, 1, len(operands))
        assert_all_numbers(operands)
        if len(operands) == 1:
            return Number(-operands[0].value)
        return Number(operands[0].value - sum(operand.value for operand in operands[1:]))


@global_attr("*")
class Multiply(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame):
        assert_all_numbers(operands)
        out = 1
        for operand in operands:
            out *= operand.value
        return Number(out)


@global_attr("/")
class Divide(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_min_callable_length(self, 1, len(operands))
        assert_all_numbers(operands)
        if len(operands) == 1:
            return Number(1 / operands[0].value)

        out = operands[0].value
        for operand in operands[1:]:
            out /= operand.value
        return Number(out)


@global_attr("abs")
class Abs(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        assert_all_numbers([operand])
        return Number(abs(operand.value))


@global_attr("expt")
class Expt(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return Number(operands[0].value ** operands[1].value)


@global_attr("modulo")
class Modulo(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return Number(operands[0].value % abs(operands[1].value))


@global_attr("quotient")
class Quotient(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        negate = (operands[0].value < 0) != (operands[1].value < 0)
        negate = -1 if negate else 1
        return Number(negate * operands[0].value // operands[1].value)


@global_attr("remainder")
class Remainder(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        negate = (operands[0].value < 0)
        negate = -1 if negate else 1
        return Number(negate * (abs(operands[0].value) % abs(operands[1].value)))


@global_attr("=")
class NumEq(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return bools[operands[0].value == operands[1].value]


@global_attr("<")
class Less(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return bools[operands[0].value < operands[1].value]


@global_attr("<=")
class LessOrEq(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return bools[operands[0].value <= operands[1].value]


@global_attr(">")
class Greater(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return bools[operands[0].value > operands[1].value]


@global_attr(">=")
class GreaterOrEq(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 2, len(operands))
        assert_all_numbers(operands)
        return bools[operands[0].value >= operands[1].value]


@global_attr("even?")
class IsEven(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        assert_all_numbers([operand])
        return bools[not operand.value % 2]


@global_attr("odd?")
class IsOdd(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        assert_all_numbers([operand])
        return bools[operand.value % 2]


@global_attr("zero?")
class IsZero(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        assert_all_numbers([operand])
        return bools[operand.value == 0]


@global_attr("not")
class Not(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        return bools[operand is SingletonFalse]


@global_attr("eq?")
class IsEq(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame):
        verify_exact_callable_length(self, 2, len(operands))
        if all(isinstance(x, ValueHolder) for x in operands):
            return bools[operands[0].value == operands[1].value]
        return bools[operands[0] is operands[1]]


@global_attr("equal?")
class IsEqual(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame):
        verify_exact_callable_length(self, 2, len(operands))
        if all(isinstance(x, ValueHolder) for x in operands):
            return bools[operands[0].value == operands[1].value]
        elif all(isinstance(x, Pair) for x in operands):
            return bools[IsEqual().execute_evaluated([operands[0].first, operands[1].first], frame) is SingletonTrue and \
                         IsEqual().execute_evaluated([operands[0].rest, operands[1].rest], frame) is SingletonTrue]
        else:
            return IsEq().execute_evaluated(operands, frame)


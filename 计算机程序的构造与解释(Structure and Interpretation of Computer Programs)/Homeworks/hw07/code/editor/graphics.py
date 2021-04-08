import math
import re
from typing import List, Optional

import log
from css_colors import COLORS
from datamodel import Expression, Number, Undefined, String, Symbol
from environment import global_attr
from evaluate_apply import Frame
from helper import verify_exact_callable_length, verify_min_callable_length
from primitives import SingleOperandPrimitive, BuiltIn
from scheme_exceptions import OperandDeduceError, IrreversibleOperationError, TurtleDrawingError

ABSOLUTE_MOVE = "M"
RELATIVE_MOVE = "m"
ABSOLUTE_LINE = "L"
RELATIVE_LINE = "l"
COMPLETE_PATH = "Z"
ABSOLUTE_ARC = "A"
RELATIVE_ARC = "a"


def make_action(command: str, *params: float) -> str:
    return command + " " + " ".join(str(param) for param in params)


def graphics_fragile(func):
    def out(*args, **kwargs):
        if log.logger.fragile:
            raise IrreversibleOperationError()
        return func(*args, **kwargs)

    return out


class Move:
    def __init__(self, stroke, fill):
        self.stroke = stroke
        self.fill = fill
        self.seq = []

    def export(self):
        return {
            "seq": " ".join(self.seq),
            "stroke": self.stroke,
            "fill": self.fill,
        }


class Canvas:
    SIZE = 1024

    def __init__(self):
        self.x = None
        self.y = None
        self.angle = None
        self.bg_color = None
        self.moves: List[Move] = None
        self.fill_move: Optional[Move] = None
        self.pen_down = None
        self.turtle_visible = True
        self.size = None

        self.reset()

    @graphics_fragile
    def set_color(self, color):
        self.moves.append(self.new_move())
        self.moves[-1].stroke = color

    @graphics_fragile
    def move(self, x: float, y: float):
        if self.pen_down:
            self.moves[-1].seq.append(make_action(ABSOLUTE_LINE, x, y))
        else:
            self.moves[-1].seq.append(make_action(ABSOLUTE_MOVE, x, y))
        if self.fill_move is not None:
            self.fill_move.seq.append(make_action(ABSOLUTE_LINE, x, y))
        self.x = x
        self.y = y

    @graphics_fragile
    def set_pixel_size(self, size: float):
        self.size = size

    @graphics_fragile
    def pixel(self, x: float, y: float, color: str):
        pixel_move = Move(color, color)
        pixel_move.seq.append(make_action(ABSOLUTE_MOVE, x * self.size, y * self.size))
        pixel_move.seq.append(make_action(RELATIVE_LINE, self.size, 0))
        pixel_move.seq.append(make_action(RELATIVE_LINE, 0, self.size))
        pixel_move.seq.append(make_action(RELATIVE_LINE, -self.size, 0))
        pixel_move.seq.append(make_action(RELATIVE_LINE, 0, -self.size))
        self.moves.insert(len(self.moves) - 1, pixel_move)

    @graphics_fragile
    def begin_fill(self):
        if self.fill_move is not None:
            raise TurtleDrawingError("Fill is already in progress.")
        self.fill_move = self.new_move()
        self.fill_move.stroke = "transparent"
        self.fill_move.fill = self.moves[-1].stroke

    @graphics_fragile
    def end_fill(self):
        if self.fill_move is None:
            raise TurtleDrawingError("No fill is currently in progress.")
        self.moves.insert(len(self.moves) - 1, self.fill_move)
        self.fill_move = None

    @graphics_fragile
    def set_bg(self, color):
        self.bg_color = color

    @graphics_fragile
    def rotate(self, theta: float):
        self.angle -= theta
        self.angle %= 360

    @graphics_fragile
    def abs_rotate(self, theta: float):
        self.angle = -theta % 360

    @graphics_fragile
    def forward(self, dist: float):
        self.move(self.x + dist * math.cos(self.angle / 360 * 2 * math.pi),
                  self.y + dist * math.sin(self.angle / 360 * 2 * math.pi))

    @graphics_fragile
    def pendown(self):
        self.pen_down = True

    @graphics_fragile
    def penup(self):
        self.pen_down = False

    # partially adapted from
    # https://stackoverflow.com/questions/5736398/how-to-calculate-the-svg-path-for-an-arc-of-a-circle
    @graphics_fragile
    def arc(self, signed_radius: float, degrees: float):
        DELTA = 0.1

        if degrees >= 360 - DELTA:
            degrees = 360 - DELTA
        elif degrees <= -360 + DELTA:
            degrees = -360 + DELTA

        def polar_to_cartesian(center_x, center_y, radius, angle_in_degrees):
            angle_in_radians = (angle_in_degrees - 90) * math.pi / 180

            return center_x + (radius * math.cos(angle_in_radians)), \
                center_y + (radius * math.sin(angle_in_radians))

        def draw_arc(x, y, radius, start_angle, end_angle):
            end_x, end_y = polar_to_cartesian(x, y, radius, end_angle)

            large_arc_flag = int(abs(degrees) > 180)
            sweep_flag = int((degrees < 0) != (signed_radius < 0))

            return make_action(ABSOLUTE_ARC, radius, radius, 0, large_arc_flag, sweep_flag, end_x, end_y), \
                end_x, \
                end_y

        center_x, center_y = polar_to_cartesian(self.x, self.y, signed_radius, self.angle)

        degree_start = self.angle + 180
        degree_end = degree_start - degrees

        arc_action, end_x, end_y = draw_arc(center_x, center_y, abs(signed_radius), degree_start, degree_end)

        self.moves[-1].seq.append(arc_action)
        if self.fill_move:
            self.fill_move.seq.append(arc_action)
        self.move(end_x, end_y)

    @graphics_fragile
    def show_turtle(self):
        self.turtle_visible = True

    @graphics_fragile
    def hide_turtle(self):
        self.turtle_visible = False

    def export(self):
        path = [move.export() for move in self.moves]
        return {
            "path": path,
            "bgColor": self.bg_color,
            "turtleX": self.x,
            "turtleY": self.y,
            "turtleRot": self.angle,
            "showTurtle": self.turtle_visible,
        }

    @graphics_fragile
    def reset(self):
        self.x = 0
        self.y = 0
        self.angle = -90
        self.bg_color = "#ffffff"
        self.moves = [self.new_move()]
        self.fill_move = None
        self.pen_down = True
        self.size = 1
        self.turtle_visible = True

    @graphics_fragile
    def new_move(self) -> Move:
        out = Move("black", "transparent")
        out.seq.append(make_action(ABSOLUTE_MOVE, self.x, self.y))
        return out


def make_color(expression: Expression) -> str:
    if not isinstance(expression, String) and not isinstance(expression, Symbol):
        raise OperandDeduceError(f"Expected a String or Symbol, received {expression}.")
    color = expression.value.lower()
    # regex from https://stackoverflow.com/questions/30241375/python-how-to-check-if-string-is-a-hex-color-code
    if color not in COLORS and not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        raise OperandDeduceError(f"Expected a valid CSS or hex color code, received {expression}.")
    return color


@global_attr("backward")
@global_attr("back")
@global_attr("bk")
class Backward(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().forward(-operand.value)
        return Undefined


@global_attr("begin_fill")
class BeginFill(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().begin_fill()
        return Undefined


@global_attr("bgcolor")
class BGColor(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression):
        log.logger.get_canvas().set_bg(make_color(operand))
        return Undefined


@global_attr("circle")
class Circle(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_min_callable_length(self, 1, len(operands))
        if len(operands) > 2:
            verify_exact_callable_length(self, 2, len(operands))
        if not isinstance(operands[0], Number):
            raise OperandDeduceError(f"Expected radius to be Number, not {operands[0]}")
        if len(operands) > 2 and not isinstance(operands[1], Number):
            raise OperandDeduceError(f"Expected angle to be Number, not {operands[1]}")
        degs = 360 if len(operands) == 1 else operands[1].value
        log.logger.get_canvas().arc(operands[0].value, degs)
        return Undefined


@global_attr("clear")
class Clear(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().reset()
        return Undefined


@global_attr("color")
class Color(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression):
        log.logger.get_canvas().set_color(make_color(operand))
        return Undefined


@global_attr("end_fill")
class EndFill(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().end_fill()
        return Undefined


@global_attr("exitonclick")
class ExitOnClick(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        return Undefined


@global_attr("forward")
@global_attr("fd")
class Forward(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().forward(operand.value)
        return Undefined


@global_attr("hideturtle")
@global_attr("ht")
class HideTurtle(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().hide_turtle()
        return Undefined


@global_attr("left")
@global_attr("lt")
class Left(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().rotate(operand.value)
        return Undefined


@global_attr("pendown")
@global_attr("pd")
class PenDown(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().pendown()
        return Undefined


@global_attr("penup")
@global_attr("pu")
class PenUp(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().penup()
        return Undefined


@global_attr("pixel")
class Pixel(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 3, len(operands))
        x, y, c, = operands
        for v in x, y:
            if not isinstance(v, Number):
                raise OperandDeduceError(f"Expected operand to be Number, not {v}")
        log.logger.get_canvas().pixel(x.value, y.value, make_color(c))
        return Undefined


@global_attr("pixelsize")
class PixelSize(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().set_pixel_size(operand.value)
        return Undefined


@global_attr("rgb")
class RGB(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 3, len(operands))
        for operand in operands:
            if not isinstance(operand, Number):
                raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
            if not 0 <= operand.value <= 1:
                raise OperandDeduceError(f"RGB values must be between 0 and 1, not {operand}")
        return String("#" + "".join('{:02X}'.format(int(x.value * 255)) for x in operands))


@global_attr("right")
@global_attr("rt")
class Right(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().rotate(-operand.value)
        return Undefined


@global_attr("screen_width")
@global_attr("screen_height")
class ScreenSize(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        return Number(log.logger.get_canvas().SIZE)


@global_attr("setheading")
@global_attr("seth")
class SetHeading(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().abs_rotate(90 - operand.value)
        return Undefined


@global_attr("setposition")
@global_attr("setpos")
@global_attr("goto")
class SetPosition(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame):
        verify_exact_callable_length(self, 2, len(operands))
        for operand in operands:
            if not isinstance(operand, Number):
                raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        log.logger.get_canvas().move(operands[0].value, -operands[1].value)
        return Undefined


@global_attr("showturtle")
@global_attr("st")
class ShowTurtle(BuiltIn):
    def execute_evaluated(self, operands: List[Expression], frame: Frame) -> Expression:
        verify_exact_callable_length(self, 0, len(operands))
        log.logger.get_canvas().show_turtle()
        return Undefined


@global_attr("speed")
class Speed(SingleOperandPrimitive):
    def execute_simple(self, operand: Expression) -> Expression:
        if not isinstance(operand, Number):
            raise OperandDeduceError(f"Expected operand to be Number, not {operand}")
        return Undefined

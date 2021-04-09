"""This module implements the built-in procedures of the Scheme language."""

from __future__ import print_function  # Python 2 compatibility

import math
import numbers
import operator
import sys
from scheme_reader import Pair, nil, repl_str


class SchemeError(Exception):
    """Exception indicating an error in a Scheme program."""

#######################
# Built-In Procedures #
#######################

# A list of triples (NAME, PYTHON-FUNCTION, INTERNAL-NAME).  Added to by
# builtin and used in scheme.create_global_frame.
BUILTINS = []

def builtin(*names):
    """An annotation to convert a Python function into a BuiltinProcedure."""
    def add(fn):
        for name in names:
            BUILTINS.append((name, fn, names[0]))
        return fn
    return add

def validate_type(val, predicate, k, name):
    """Returns VAL.  Raises a SchemeError if not PREDICATE(VAL)
    using "argument K of NAME" to describe the offending value."""
    if not predicate(val):
        msg = "argument {0} of {1} has wrong type ({2})"
        type_name = type(val).__name__
        if scheme_symbolp(val):
            type_name = "symbol"
        raise SchemeError(msg.format(k, name, type_name))
    return val

@builtin("boolean?")
def scheme_booleanp(x):
    return x is True or x is False

def is_true_primitive(val):
    """All values in Scheme are true except False."""
    return val is not False

def is_false_primitive(val):
    """Only False is false in scheme_reader."""
    return val is False

@builtin("not")
def scheme_not(x):
    return not is_true_primitive(x)

@builtin("equal?")
def scheme_equalp(x, y):
    if scheme_pairp(x) and scheme_pairp(y):
        return scheme_equalp(x.first, y.first) and scheme_equalp(x.rest, y.rest)
    elif scheme_numberp(x) and scheme_numberp(y):
        return x == y
    else:
        return type(x) == type(y) and x == y

@builtin("eq?")
def scheme_eqp(x, y):
    if scheme_numberp(x) and scheme_numberp(y):
        return x == y
    elif scheme_symbolp(x) and scheme_symbolp(y):
        return x == y
    else:
        return x is y

@builtin("pair?")
def scheme_pairp(x):
    return type(x).__name__ == 'Pair'

@builtin("scheme-valid-cdr?")
def scheme_valid_cdrp(x):
    return scheme_pairp(x) or scheme_nullp(x) or scheme_promisep(x)

# Streams
@builtin("promise?")
def scheme_promisep(x):
    return type(x).__name__ == 'Promise'

@builtin("force")
def scheme_force(x):
    validate_type(x, scheme_promisep, 0, 'promise')
    return x.evaluate()

@builtin("cdr-stream")
def scheme_cdr_stream(x):
    validate_type(x, lambda x: scheme_pairp(x) and scheme_promisep(x.rest), 0, 'cdr-stream')
    return scheme_force(x.rest)

@builtin("null?")
def scheme_nullp(x):
    return type(x).__name__ == 'nil'

@builtin("list?")
def scheme_listp(x):
    """Return whether x is a well-formed list. Assumes no cycles."""
    while x is not nil:
        if not isinstance(x, Pair):
            return False
        x = x.rest
    return True

@builtin("length")
def scheme_length(x):
    validate_type(x, scheme_listp, 0, 'length')
    if x is nil:
        return 0
    return len(x)

@builtin("cons")
def scheme_cons(x, y):
    return Pair(x, y)

@builtin("car")
def scheme_car(x):
    validate_type(x, scheme_pairp, 0, 'car')
    return x.first

@builtin("cdr")
def scheme_cdr(x):
    validate_type(x, scheme_pairp, 0, 'cdr')
    return x.rest

# Mutation extras
@builtin("set-car!")
def scheme_set_car(x, y):
    validate_type(x, scheme_pairp, 0, 'set-car!')
    x.first = y

@builtin("set-cdr!")
def scheme_set_cdr(x, y):
    validate_type(x, scheme_pairp, 0, 'set-cdr!')
    validate_type(y, scheme_valid_cdrp, 1, 'set-cdr!')
    x.rest = y

@builtin("list")
def scheme_list(*vals):
    result = nil
    for e in reversed(vals):
        result = Pair(e, result)
    return result

@builtin("append")
def scheme_append(*vals):
    if len(vals) == 0:
        return nil
    result = vals[-1]
    for i in range(len(vals)-2, -1, -1):
        v = vals[i]
        if v is not nil:
            validate_type(v, scheme_pairp, i, 'append')
            r = p = Pair(v.first, result)
            v = v.rest
            while scheme_pairp(v):
                p.rest = Pair(v.first, result)
                p = p.rest
                v = v.rest
            result = r
    return result

@builtin("string?")
def scheme_stringp(x):
    return isinstance(x, str) and x.startswith('"')

@builtin("symbol?")
def scheme_symbolp(x):
    return isinstance(x, str) and not scheme_stringp(x)


@builtin("number?")
def scheme_numberp(x):
    return isinstance(x, numbers.Real) and not scheme_booleanp(x)

@builtin("integer?")
def scheme_integerp(x):
    return scheme_numberp(x) and (isinstance(x, numbers.Integral) or int(x) == x)

def _check_nums(*vals):
    """Check that all arguments in VALS are numbers."""
    for i, v in enumerate(vals):
        if not scheme_numberp(v):
            msg = "operand {0} ({1}) is not a number"
            raise SchemeError(msg.format(i, v))

def _arith(fn, init, vals):
    """Perform the FN operation on the number values of VALS, with INIT as
    the value when VALS is empty. Returns the result as a Scheme value."""
    _check_nums(*vals)
    s = init
    for val in vals:
        s = fn(s, val)
    s = _ensure_int(s)
    return s

def _ensure_int(x):
    if int(x) == x:
        x = int(x)
    return x

@builtin("+")
def scheme_add(*vals):
    return _arith(operator.add, 0, vals)

@builtin("-")
def scheme_sub(val0, *vals):
    _check_nums(val0, *vals) # fixes off-by-one error
    if len(vals) == 0:
        return _ensure_int(-val0)
    return _arith(operator.sub, val0, vals)

@builtin("*")
def scheme_mul(*vals):
    return _arith(operator.mul, 1, vals)

@builtin("/")
def scheme_div(val0, *vals):
    _check_nums(val0, *vals) # fixes off-by-one error
    try:
        if len(vals) == 0:
            return _ensure_int(operator.truediv(1, val0))
        return _arith(operator.truediv, val0, vals)
    except ZeroDivisionError as err:
        raise SchemeError(err)

@builtin("expt")
def scheme_expt(val0, val1):
    _check_nums(val0, val1)
    return pow(val0, val1)

@builtin("abs")
def scheme_abs(val0):
    return abs(val0)

@builtin("quotient")
def scheme_quo(val0, val1):
    _check_nums(val0, val1)
    try:
        return -(-val0 // val1) if (val0 < 0) ^ (val1 < 0) else val0 // val1
    except ZeroDivisionError as err:
        raise SchemeError(err)

@builtin("modulo")
def scheme_modulo(val0, val1):
    _check_nums(val0, val1)
    try:
        return val0 % val1
    except ZeroDivisionError as err:
        raise SchemeError(err)

@builtin("remainder")
def scheme_remainder(val0, val1):
    _check_nums(val0, val1)
    try:
        result = val0 % val1
    except ZeroDivisionError as err:
        raise SchemeError(err)
    while result < 0 and val0 > 0 or result > 0 and val0 < 0:
        result -= val1
    return result

def number_fn(module, name, fallback=None):
    """A Scheme built-in procedure that calls the numeric Python function named
    MODULE.FN."""
    py_fn = getattr(module, name) if fallback is None else getattr(module, name, fallback)
    def scheme_fn(*vals):
        _check_nums(*vals)
        return py_fn(*vals)
    return scheme_fn

# Add number functions in the math module as built-in procedures in Scheme
for _name in ["acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh",
              "ceil", "copysign", "cos", "cosh", "degrees", "floor", "log",
              "log10", "log1p", "radians", "sin", "sinh", "sqrt",
              "tan", "tanh", "trunc"]:
    builtin(_name)(number_fn(math, _name))
builtin("log2")(number_fn(math, "log2", lambda x: math.log(x, 2)))  # Python 2 compatibility

def _numcomp(op, x, y):
    _check_nums(x, y)
    return op(x, y)

@builtin("=")
def scheme_eq(x, y):
    return _numcomp(operator.eq, x, y)

@builtin("<")
def scheme_lt(x, y):
    return _numcomp(operator.lt, x, y)

@builtin(">")
def scheme_gt(x, y):
    return _numcomp(operator.gt, x, y)

@builtin("<=")
def scheme_le(x, y):
    return _numcomp(operator.le, x, y)

@builtin(">=")
def scheme_ge(x, y):
    return _numcomp(operator.ge, x, y)

@builtin("even?")
def scheme_evenp(x):
    _check_nums(x)
    return x % 2 == 0

@builtin("odd?")
def scheme_oddp(x):
    _check_nums(x)
    return x % 2 == 1

@builtin("zero?")
def scheme_zerop(x):
    _check_nums(x)
    return x == 0

##
## Other operations
##

@builtin("atom?")
def scheme_atomp(x):
    return (scheme_booleanp(x) or scheme_numberp(x) or scheme_symbolp(x) or
            scheme_nullp(x) or scheme_stringp(x))

@builtin("display")
def scheme_display(*vals):
    vals = [repl_str(eval(val) if scheme_stringp(val) else val) for val in vals]
    print(*vals, end="")

@builtin("print")
def scheme_print(*vals):
    vals = [repl_str(val) for val in vals]
    print(*vals)

@builtin("displayln")
def scheme_displayln(*vals):
    scheme_display(*vals)
    scheme_newline()

@builtin("newline")
def scheme_newline():
    print()
    sys.stdout.flush()

@builtin("error")
def scheme_error(msg=None):
    msg = "" if msg is None else repl_str(msg)
    raise SchemeError(msg)

@builtin("exit")
def scheme_exit():
    raise EOFError

##
## Turtle graphics (non-standard)
##

turtle = CANVAS = None

def _title():
    import turtle as _nativeturtle
    _nativeturtle.title("Scheme Turtles")

def attempt_install_tk_turtle():
    try:
        from abstract_turtle import turtle
    except ImportError:
        raise SchemeError("Could not find abstract_turtle. This should never happen in student-facing situations. If you are a student, please file a bug on Piazza.")
    return turtle

def attempt_create_tk_canvas():
    try:
        import tkinter as _
    except:
        raise SchemeError("\n".join([
            "Could not import tkinter, so the tk-turtle will not work.",
            "Either install python with tkinter support or run in pillow-turtle mode"
        ]))
    from abstract_turtle import TkCanvas
    return TkCanvas(1000, 1000, init_hook=_title)

def attempt_create_pillow_canvas():
    try:
        import PIL as _
        import numpy as _
    except:
        raise SchemeError("\n".join([
            "Could not import abstract_turtle[pillow_canvas]'s dependencies.",
            "To install these packages, run",
            "    python3 -m pip install 'abstract_turtle[pillow_canvas]'",
            "You can also run in tk-turtle mode by removing the flag `--pillow-turtle`"
        ]))
    from abstract_turtle import PillowCanvas
    return PillowCanvas(1000, 1000)

def _tscheme_prep():
    global turtle, CANVAS
    if turtle is not None:
        return
    _turtle = attempt_install_tk_turtle()
    if builtins.TK_TURTLE:
        try:
            _CANVAS = attempt_create_tk_canvas()
        except SchemeError as e:
            print(e, file=sys.stderr)
            print("Attempting pillow canvas mode", file=sys.stderr)
            _CANVAS = attempt_create_pillow_canvas()
    else:
        _CANVAS = attempt_create_pillow_canvas()
    turtle, CANVAS = _turtle, _CANVAS
    turtle.set_canvas(CANVAS)
    turtle.mode("logo")


@builtin("forward", "fd")
def tscheme_forward(n):
    """Move the turtle forward a distance N units on the current heading."""
    _check_nums(n)
    _tscheme_prep()
    turtle.forward(n)

@builtin("backward", "back", "bk")
def tscheme_backward(n):
    """Move the turtle backward a distance N units on the current heading,
    without changing direction."""
    _check_nums(n)
    _tscheme_prep()
    turtle.backward(n)

@builtin("left", "lt")
def tscheme_left(n):
    """Rotate the turtle's heading N degrees counterclockwise."""
    _check_nums(n)
    _tscheme_prep()
    turtle.left(n)

@builtin("right", "rt")
def tscheme_right(n):
    """Rotate the turtle's heading N degrees clockwise."""
    _check_nums(n)
    _tscheme_prep()
    turtle.right(n)

@builtin("circle")
def tscheme_circle(r, extent=None):
    """Draw a circle with center R units to the left of the turtle (i.e.,
    right if N is negative.  If EXTENT is not None, then draw EXTENT degrees
    of the circle only.  Draws in the clockwise direction if R is negative,
    and otherwise counterclockwise, leaving the turtle facing along the
    arc at its end."""
    if extent is None:
        _check_nums(r)
    else:
        _check_nums(r, extent)
    _tscheme_prep()
    turtle.circle(r, extent and extent)

@builtin("setposition", "setpos", "goto")
def tscheme_setposition(x, y):
    """Set turtle's position to (X,Y), heading unchanged."""
    _check_nums(x, y)
    _tscheme_prep()
    turtle.setposition(x, y)

@builtin("setheading", "seth")
def tscheme_setheading(h):
    """Set the turtle's heading H degrees clockwise from north (up)."""
    _check_nums(h)
    _tscheme_prep()
    turtle.setheading(h)

@builtin("penup", "pu")
def tscheme_penup():
    """Raise the pen, so that the turtle does not draw."""
    _tscheme_prep()
    turtle.penup()

@builtin("pendown", "pd")
def tscheme_pendown():
    """Lower the pen, so that the turtle starts drawing."""
    _tscheme_prep()
    turtle.pendown()

@builtin("showturtle", "st")
def tscheme_showturtle():
    """Make turtle visible."""
    _tscheme_prep()
    turtle.showturtle()

@builtin("hideturtle", "ht")
def tscheme_hideturtle():
    """Make turtle visible."""
    _tscheme_prep()
    turtle.hideturtle()

@builtin("clear")
def tscheme_clear():
    """Clear the drawing, leaving the turtle unchanged."""
    _tscheme_prep()
    turtle.clear()

@builtin("color")
def tscheme_color(c):
    """Set the color to C, a string such as '"red"' or '"#ffc0c0"' (representing
    hexadecimal red, green, and blue values."""
    _tscheme_prep()
    validate_type(c, scheme_stringp, 0, "color")
    turtle.color(eval(c))

@builtin("rgb")
def tscheme_rgb(red, green, blue):
    """Return a color from RED, GREEN, and BLUE values from 0 to 1."""
    colors = (red, green, blue)
    for x in colors:
        if x < 0 or x > 1:
            raise SchemeError("Illegal color intensity in " + repl_str(colors))
    scaled = tuple(int(x*255) for x in colors)
    return '"#%02x%02x%02x"' % scaled

@builtin("begin_fill")
def tscheme_begin_fill():
    """Start a sequence of moves that outline a shape to be filled."""
    _tscheme_prep()
    turtle.begin_fill()

@builtin("end_fill")
def tscheme_end_fill():
    """Fill in shape drawn since last begin_fill."""
    _tscheme_prep()
    turtle.end_fill()

@builtin("bgcolor")
def tscheme_bgcolor(c):
    _tscheme_prep()
    validate_type(c, scheme_stringp, 0, "bgcolor")
    turtle.bgcolor(eval(c))

@builtin("exitonclick")
def tscheme_exitonclick():
    global turtle
    """Wait for a click on the turtle window, and then close it."""
    if turtle is None:
        return
    _tscheme_prep()
    # BEGIN SOLUTION NO PROMPT ALT="if _turtle_screen_on:"
    if builtins.TK_TURTLE:
        print("Close or click on turtle window to complete exit")
    if builtins.TURTLE_SAVE_PATH is not None:
        _save(builtins.TURTLE_SAVE_PATH)
    turtle.exitonclick()
    turtle = None

@builtin("speed")
def tscheme_speed(s):
    """Set the turtle's animation speed as indicated by S (an integer in
    0-10, with 0 indicating no animation (lines draw instantly), and 1-10
    indicating faster and faster movement."""
    validate_type(s, scheme_integerp, 0, "speed")
    _tscheme_prep()
    turtle.speed(s)

@builtin("pixel")
def tscheme_pixel(x, y, c):
    """Draw a filled box of pixels (default 1 pixel) at (X, Y) in color C."""
    validate_type(c, scheme_stringp, 0, "pixel")
    color = eval(c)
    _tscheme_prep()
    turtle.pixel(x, y, color)

@builtin("pixelsize")
def tscheme_pixelsize(size):
    """Change pixel size to SIZE."""
    _check_nums(size)
    _tscheme_prep()
    turtle.pixel_size(size)

@builtin("screen_width")
def tscheme_screen_width():
    """Screen width in pixels of the current size (default 1)."""
    _tscheme_prep()
    return turtle.canvas_width()

@builtin("screen_height")
def tscheme_screen_height():
    """Screen height in pixels of the current size (default 1)."""
    _tscheme_prep()
    return turtle.canvas_height()

def _save(path):
    if not builtins.TK_TURTLE:
        path = path + ".png"
        CANVAS.export().save(path, "png")
    else:
        CANVAS.export(path + ".ps")

@builtin("save-to-file")
def tscheme_write_to_file(path):
    _tscheme_prep()
    validate_type(path, scheme_stringp, 0, "save-to-file")
    path = eval(path)
    _save(path)
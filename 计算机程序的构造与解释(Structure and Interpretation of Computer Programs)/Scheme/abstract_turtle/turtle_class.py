from functools import wraps
from math import pi, sin, cos, copysign

from .model import Color, Position, DrawnTurtle, Mode, LineTo, Arc
from .canvas import Canvas

def turtle_method(func):
    """
    Marks the given method as one that needs to be placed in global.
    """
    func.is_turtle_method = True
    return func


def make_formode():
    handlers = {}

    def formode(mode):
        def decorator(func):
            @wraps(func)
            def error(self, *args, **kwargs):
                raise RuntimeError(
                    "Handler not available for mode: {}".format(self._BaseTurtle__mode)
                )

            prev = handlers.get(func.__name__, error)

            @wraps(func)
            def handler(self, *args, **kwargs):
                if self._BaseTurtle__mode == mode:
                    return func(self, *args, **kwargs)
                else:
                    return prev(self, *args, **kwargs)

            handlers[func.__name__] = handler

            return handler

        return decorator

    return formode


formode = make_formode()


class BaseTurtle:
    """
    Manages all the basic turtle functionality. The other turtle methods can be expressed in terms of these.
    """
    def __init__(self, canvas):
        if not isinstance(canvas, Canvas):
            raise RuntimeError("Expected the argument to Turtle to be of type {} but was {} of type {}".format(
                Canvas.__name__,
                canvas,
                type(canvas).__name__
            ))
        self.__canvas = canvas
        self.__x = 0
        self.__y = 0
        self.__line_width = 1
        self.__theta = 0
        self.__pen_color = Color(0, 0, 0)
        self.__fill_color = Color(0, 0, 0)
        self.__pen_down = True
        self.__degrees = 360
        self.__path = None
        self.__turtle_is_shown = True
        self.__turtle_stretch_wid = 1
        self.__turtle_stretch_len = 1
        self.__pixel_size = 1
        self.__mode = Mode.STANDARD
        self.__speed = 3 # default from the normal turtle module

        self.__update_turtle()

    @turtle_method
    def goto(self, x, y):
        """
        Go to the given position (X, Y).
        """
        if self.__pen_down:
            self.__canvas.draw_line(self.__current_pos, Position(x, y), self.__pen_color, self.__line_width)
        self.__x = x
        self.__y = y
        if self.filling():
            self.__path.append(LineTo(self.__current_pos))
        self.__update_turtle()
    setpos = setposition = goto

    @turtle_method
    def forward(self, amount):
        """
        Move forward the given amount.
        """
        self.goto(self.xcor() + amount * cos(self.__theta), self.ycor() + amount * sin(self.__theta))
    fd = forward

    @turtle_method
    def setheading(self, heading):
        """
        Set the heading to the given value in degrees
        """
        self.__theta = self.__to_real_angle(heading)
        self.__update_turtle()
    seth = setheading

    @turtle_method
    def circle(self, radius, extent=None):
        """
        Draw a circle starting at the given point with the given RADIUS and EXTENT. If EXTENT exists, draw only the
        first EXTENT degrees of the circle. If RADIUS is positive, draw in the counterclockwise direction.
        Otherwise, draw in the clockwise direction.
        """
        if extent is None:
            extent = self.__degrees

        extent = extent / self.__degrees * (2 * pi)

        center = Position(
            self.__current_pos.x - radius * sin(self.__theta),
            self.__current_pos.y + radius * cos(self.__theta),
        )
        angle_change = copysign(1, radius) * extent
        start_angle = self.__theta - pi / 2 * copysign(1, radius)
        end_angle = start_angle + angle_change

        if self.filling():
            self.__path.append(Arc(center, abs(radius), start_angle, end_angle))

        if self.__pen_down:
            if radius * extent < 0:
                start_angle, end_angle = end_angle, start_angle
            self.__canvas.draw_circle(center, abs(radius), self.__pen_color, self.__line_width, False, start_angle,
                                      end_angle)

        final_pos = Position(
            center.x + radius * sin(self.__theta + angle_change),
            center.y - radius * cos(self.__theta + angle_change),
        )
        self.__theta += angle_change
        self.__x, self.__y = final_pos.x, final_pos.y
        self.__update_turtle()

    @turtle_method
    def dot(self, size=None):
        """
        Draw a dot at the current location. If size is not specified, set it to
            (pensize + 4, pensize * 2)
        """
        if size is None:
            size = max(self.__line_width + 4, self.__line_width * 2)
        if self.__pen_down:
            self.__canvas.draw_circle(self.__current_pos, size, self.__pen_color, self.__line_width, True, 0, 2 * pi)

    @turtle_method
    def pixel(self, x, y, *color):
        """
        Fill in a square of size pixel_size at (x * pixel_size, y * pixel_size) with the given color.
        """
        d = self.__pixel_size
        self.__canvas.axis_aligned_rectangle(
            Position(x * d, y * d),
            d, d,
            self.__convert_color(*color)
        )

    @turtle_method
    def pixel_size(self, pixel_size):
        if not isinstance(pixel_size, int) or pixel_size <= 0:
            raise ValueError("Expected a positive integer for pixel_size but got {}".format(pixel_size))
        self.__pixel_size = pixel_size

    @turtle_method
    def canvas_width(self):
        """
        Return the current screen size in pixel units
        """
        return self.__canvas.width // self.__pixel_size

    @turtle_method
    def canvas_height(self):
        """
        Return the current screen size in pixel units
        """
        return self.__canvas.height // self.__pixel_size

    @turtle_method
    def xcor(self):
        """
        Get the current x coordinate
        """
        return self.__x

    @turtle_method
    def ycor(self):
        """
        Get the current y coordinate
        """
        return self.__y

    @turtle_method
    def heading(self):
        """
        Get the current heading
        """
        return self.__from_real_angle(self.__theta)

    @turtle_method
    def degrees(self, amount=360):
        """
        Set the number of degrees in a circle
        """
        self.__degrees = amount

    @turtle_method
    def pendown(self):
        """
        Do draw when moving
        """
        self.__pen_down = True
    pd = down = pendown

    @turtle_method
    def penup(self):
        """
        Do not draw when moving
        """
        self.__pen_down = False
    pu = up = penup

    @turtle_method
    def pensize(self, width=None):
        """
        Set or get the pen size. If WIDTH is None, get it, otherwise set it.
        """
        if width is None:
            return self.__line_width
        self.__line_width = width
    width = pensize

    @turtle_method
    def isdown(self):
        """
        Return if the pen is down or not
        """
        return self.__pen_down

    @turtle_method
    def pencolor(self, *color):
        """
        Set the pen color as COLOR
        """
        self.__pen_color = self.__convert_color(*color)

    @turtle_method
    def fillcolor(self, *color):
        """
        Set the fill color as COLOR
        """
        self.__fill_color = self.__convert_color(*color)

    @turtle_method
    def filling(self):
        """
        Return whether the canvas is filling.
        """
        return self.__path is not None

    @turtle_method
    def begin_fill(self):
        """
        Begin setting the polygon to fill
        """
        self.__path = [LineTo(self.__current_pos)]

    @turtle_method
    def end_fill(self):
        """
        End setting the polygon to fill, and fill it in.
        """
        if self.__path is None:
            return
        self.__canvas.fill_path(self.__path, self.__fill_color)
        self.__path = None

    @turtle_method
    def clear(self):
        """
        Clear the canvas, but do not move the turtle.
        """
        self.__canvas.clear()

    @turtle_method
    def bgcolor(self, *color):
        self.__canvas.set_bgcolor(self.__convert_color(*color))

    def __update_turtle(self):
        if self.__turtle_is_shown:
            self.__canvas.turtle = DrawnTurtle(self.__current_pos, self.__theta % (2 * pi), self.__turtle_stretch_wid, self.__turtle_stretch_len)
        else:
            self.__canvas.turtle = None

    @turtle_method
    def hideturtle(self):
        """
        Hide the turtle from the canvas.
        """
        self.__turtle_is_shown = False
        self.__update_turtle()
    ht = hideturtle

    @turtle_method
    def showturtle(self):
        """
        Show the turtle on the canvas
        """
        self.__turtle_is_shown = True
        self.__update_turtle()
    st = showturtle

    @turtle_method
    def isvisible(self):
        """
        Return whether the turtle is visible
        """
        return self.__turtle_is_shown

    @turtle_method
    def shapesize(self, stretch_wid=None, stretch_len=None):
        self.__turtle_stretch_wid = stretch_wid
        self.__turtle_stretch_len = stretch_len
        self.__update_turtle()
    turtlesize = shapesize

    @turtle_method
    def mode(self, mode=None):
        if mode is None:
            return self.__mode.value
        elif mode == "standard":
            self.__mode = Mode.STANDARD
        elif mode == "logo":
            self.__mode = Mode.LOGO
        elif mode == "world":
            raise RuntimeError("Custom world coordinates not supported.")
        else:
            raise RuntimeError("Unknown mode: {}".format(mode))
        self.goto(0, 0)
        self.setheading(0)
        self.clear()

    @turtle_method
    def speed(self, speed=None):
        if speed is None:
            return self.__speed
        self.__speed = speed
        self.__canvas.set_speed(speed)

    @turtle_method
    def exitonclick(self):
        return self.__canvas.exit_on_click()

    @property
    def __current_pos(self):
        return Position(self.__x, self.__y)

    @formode(Mode.STANDARD)
    def __to_real_angle(self, amount):
        return (amount / self.__degrees) * (2 * pi)

    @formode(Mode.STANDARD)
    def __from_real_angle(self, angle):
        return (angle / (2 * pi)) * self.__degrees % self.__degrees

    @formode(Mode.LOGO)
    def __to_real_angle(self, amount):
        return (1 / 4 - amount / self.__degrees) * (2 * pi)

    @formode(Mode.LOGO)
    def __from_real_angle(self, angle):
        return (1 / 4 - angle / (2 * pi)) * self.__degrees % self.__degrees

    @staticmethod
    def __convert_color(*color):
        return Color.of(*color)


class Turtle(BaseTurtle):
    """
    This entire class should only use public methods of the BaseTurtle class.
    """

    @turtle_method
    def backward(self, amount):
        """
        Move backward the given amount.
        """
        self.forward(-amount)
    bk = back = backward

    @formode(Mode.STANDARD)
    def right(self, amount):
        self.setheading(self.heading() - amount)

    @turtle_method
    @formode(Mode.LOGO)
    def right(self, amount):
        """
        Rotate right the given amount.
        """
        self.setheading(self.heading() + amount)

    rt = right

    @turtle_method
    def left(self, amount):
        """
        Rotate left the given amount.
        """
        self.right(-amount)
    lt = left

    @turtle_method
    def setx(self, x):
        """
        Move so that the x coordinate is X
        """
        self.goto(x, self.xcor())

    @turtle_method
    def sety(self, y):
        """
        Move so that the y coordinate is Y
        """
        self.goto(self.xcor(), y)

    @turtle_method
    def home(self):
        """
        Set location to (0, 0) and set heading to 0
        """
        self.goto(0, 0)
        self.setheading(0)

    @turtle_method
    def position(self):
        """
        Get the current position as a tuple
        """
        return self.xcor(), self.ycor()
    pos = position

    @turtle_method
    def distance(self, other):
        """
        Get the distance between this and the other location/turtle.
        """
        if isinstance(other, Turtle):
            return self.distance(other.position())
        x, y = other
        return ((x - self.xcor()) ** 2 + (y - self.ycor()) ** 2) ** 0.5

    @turtle_method
    def radians(self):
        """
        Set angle units to radians
        """
        return self.degrees(2 * pi)

    @turtle_method
    def color(self, *color):
        """
        Set both the pen and fill colors
        """
        self.pencolor(*color)
        self.fillcolor(*color)

    @turtle_method
    def reset(self):
        self.home()
        self.clear()


from abc import ABC, abstractmethod
from math import pi


class Canvas(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._turtle = None

    @property
    def turtle(self):
        return self._turtle

    @turtle.setter
    def turtle(self, turtle):
        self._turtle = turtle
        self.refreshed_turtle(turtle)

    @abstractmethod
    def draw_rectangular_line(self, start, end, color, width):
        """
        Draw a 1 width line from START to END with the given color COLOR
        """
        pass

    def draw_line(self, start, end, color, width):
        if width > 1:
            self.draw_circle(start, width / 2, color, width, True, 0, 2 * pi)
        self.draw_rectangular_line(start, end, color, width)
        if width > 1:
            self.draw_circle(end, width / 2, color, width, True, 0, 2 * pi)

    @abstractmethod
    def draw_circle(self, center, radius, color, width, is_filled, start, end):
        """
        Draw a circle of width 1 with the given center CENTER, radius RADIUS, and color COLOR.
        Only draw the portion with angle between START and END, moving counterclockwise from START to END.
        RADIUS must be non-negative.

        Fill the circle if IS_FILLED is true.
        """
        pass

    @abstractmethod
    def fill_path(self, path, color):
        """
        Fill the given polygon formed by the movements in PATH using fill color COLOR.
        """
        pass

    @abstractmethod
    def axis_aligned_rectangle(self, bottom_left, width, height, color):
        """
        Fill the given rectangle with bottom left corner BOTTOM_LEFT, and dimensions (WIDTH, HEIGHT),
            and fill color COLOR
        """
        pass

    @abstractmethod
    def set_bgcolor(self, color):
        """
        Fill the entire background with the given COLOR
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clear everything in the foreground
        """
        pass

    @abstractmethod
    def refreshed_turtle(self, drawn_turtle):
        """
        Update the turtle to the given DrawnTurtle object, or remove the turtle if None is passed
        """
        pass

    @abstractmethod
    def set_speed(self, speed):
        """
        Set the animation speed, should be consistent with the built-in turtle module if implemented at all.
        """
        pass

    @abstractmethod
    def exit_on_click(self):
        """
        Blocks until a click, upon which the GUI is closed.
        For non-gui apps, this does nothing, but GUI based apps should change the behavior.
        """
        pass

from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum

from math import sin, cos

from .color_names import COLORS


class Color(namedtuple('Color', ['red', 'green', 'blue'])):
    @staticmethod
    def of(*color):
        if len(color) == 3 and all(isinstance(c, int) for c in color):
            if not all(0 <= c < 256 for c in color):
                raise RuntimeError("Invalid integer color: {!r}".format(color))
            return Color(*color)
        if len(color) == 1 and isinstance(color[0], str):
            color = color[0].lower()
            if color and color[0] == "#":
                return Color.hexcolor(color[1:])
            color = color.replace(" ", "").replace("_", "")
            if color in COLORS:
                return Color.of(COLORS[color])
            raise RuntimeError("Invalid color string: {!r}".format(color))
        types = [type(c).__name__ for c in color]
        raise RuntimeError("Invalid color. Expected either 3 ints or 1 string, but got: {}".format(", ".join(types)))

    @staticmethod
    def hexcolor(color):
        if len(color) == 3:  # shorthand hex
            color = "".join(x * 2 for x in color)
        if len(color) == 6:
            vals = [Color.hexparse(color[i:i+2]) for i in range(0, 6, 2)]
            if all(x is not None for x in vals):
                return Color.of(*vals)
        raise RuntimeError("Invalid hex color string: {!r}".format(color))

    @staticmethod
    def hexparse(pair):
        try:
            return int(pair, 16)
        except ValueError:
            return None


Position = namedtuple('Position', ['x', 'y'])

class DrawnTurtle(namedtuple('DrawnTurtle', ['pos', 'heading', 'stretch_wid', 'stretch_len'])):
    @property
    def points(self):
        unadjusted_points = [
            (-3, 8),
            (0, 0),
            (-3, -8),
            (8, 0),
        ]
        stretched_points = [
            (dx * self.stretch_len, dy * self.stretch_wid) for dx, dy in unadjusted_points
        ]
        rotated_points = [
            rotate(*dxy, self.heading) for dxy in stretched_points
        ]
        moved_points = [
            Position(self.pos.x + dx, self.pos.y + dy) for dx, dy in rotated_points
        ]
        return moved_points

    @property
    def json_friendly(self):
        return [
            [self.pos.x, self.pos.y],
            self.heading,
            self.stretch_wid,
            self.stretch_len
        ]


class Mode(Enum):
    LOGO = "logo"
    STANDARD = "standard"


def rotate(x, y, theta):
    return x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta)


class Path(ABC):
    @abstractmethod
    def to_points(self, divisions=100):
        """
        Return an iterable of points corresponding to this path element
        """

    @property
    @abstractmethod
    def json_friendly(self):
        """
        Converts the given path to a JSON compatible object.
        """


class LineTo(Path, namedtuple("LineTo", ["position"])):
    def to_points(self, divisions=100):
        del divisions
        return [self.position]

    @property
    def json_friendly(self):
        return ["line", self.position]


class Arc(Path, namedtuple("Arc", ["center", "radius", "start_angle", "end_angle"])):
    """
    CENTER is the center of the arc
    START_ANGLE and END_ANGLE are the starting and ending angles of the arc measured in radians CCW from the x-axis
    """

    def to_points(self, divisions=100):
        for i in range(divisions + 1):
            ang = self.start_angle + (i / divisions) * (self.end_angle - self.start_angle)
            yield Position(self.center.x + self.radius * cos(ang), self.center.y + self.radius * sin(ang))

    @property
    def json_friendly(self):
        return ["arc", self.center, self.radius, self.start_angle, self.end_angle]


from abc import abstractmethod
from math import pi

from .canvas import Canvas

class AbstractLoggingCanvas(Canvas):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.drawn_turtle = None

    @abstractmethod
    def on_action(self, log_line):
        pass

    def draw_rectangular_line(self, start, end, color, width):
        self.on_action(['draw_rectangular_line', [start.x, start.y, end.x, end.y], color, width])

    def draw_circle(self, center, radius, color, width, is_filled, start, end):
        self.on_action(['draw_circle', [center.x, center.y, radius], color, width, is_filled, start, end])

    def fill_path(self, path, color):
        self.on_action(['fill_path', [edge.json_friendly for edge in path], color])

    def axis_aligned_rectangle(self, bottom_left, width, height, color):
        self.on_action(['axis_aligned_rectangle', [bottom_left.x, bottom_left.y], width, height, color])

    def set_bgcolor(self, color):
        self.on_action(['set_bgcolor', color])

    def clear(self):
        self.on_action(['clear'])

    def refreshed_turtle(self, drawn_turtle):
        self.on_action([
            'refreshed_turtle',
            drawn_turtle.json_friendly if drawn_turtle is not None else None
        ])
        self.drawn_turtle = drawn_turtle

    def set_speed(self, speed):
        self.on_action(['set_speed', speed])

    def exit_on_click(self):
        self.on_action(['exit_on_click'])

class LoggingCanvas(AbstractLoggingCanvas):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.log = []
    def on_action(self, log_line):
        self.log.append(log_line)


from math import sin, cos, pi
try:
    from PIL import Image, ImageDraw
    import numpy as np
except ImportError:
    pass

from .canvas import Canvas
from .model import Color, Position


class PillowCanvas(Canvas):
    """
    Draw the given results on a pillow canvas.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = Image.new('RGBA', (width, height))
        self.background_color = Color(255, 255, 255)
        self.draw = ImageDraw.Draw(self.image)
        self.turtle = None

    def tr_pos(self, pos):
        x, y = pos.x, pos.y
        return np.round(x + self.width / 2), np.round(-y + self.height / 2)

    @staticmethod
    def tr_color(color):
        return color.red, color.green, color.blue, 255

    def draw_rectangular_line(self, start, end, color, width):
        self.draw.line([self.tr_pos(start), self.tr_pos(end)], self.tr_color(color), width)

    def draw_circle(self, center, radius, color, width, is_filled, start, end):
        x, y = self.tr_pos(center)
        left_up = (x-radius, y-radius)
        right_down = (x+radius, y+radius)
        box = [left_up, right_down]
        if is_filled:
            assert start == 0
            assert end == 2 * pi
            self.draw.ellipse(box, fill=self.tr_color(color))
        else:
            self.draw.arc(box, -end * 180 / pi, -start * 180 / pi, fill=self.tr_color(color), width=width)

    def fill_path(self, path, color):
        points = []
        for movement in path:
            points += movement.to_points()
        self.draw.polygon(
            [self.tr_pos(point) for point in points],
            fill=self.tr_color(color)
        )

    def axis_aligned_rectangle(self, bottom_left, width, height, color):
        blx, bly = self.tr_pos(bottom_left)
        # bounding box in pixel space, make this exactly w*h
        # subtract one to have blx, blx+1, ..., blx+w-1, etc.
        tlx, tly = blx + (width - 1), bly - (height - 1)
        bounding_box = [blx, bly, tlx, tly]
        print(bounding_box)
        self.draw.rectangle(
            bounding_box,
            fill=self.tr_color(color)
        )

    def set_bgcolor(self, color):
        self.background_color = color

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0, 0))

    def export(self):
        image = self.image.copy()
        if self.turtle is not None:
            ImageDraw.Draw(image).polygon(
                [self.tr_pos(point) for point in self.turtle.points],
                fill=self.tr_color(Color.of(0, 0, 0))
            )
        data = np.array(image)
        assert len(data.shape) == 3 and data.shape[-1] == 4
        transparents = data[:,:,-1] == 0
        data[transparents] = self.tr_color(self.background_color)
        return Image.fromarray(data)

    def refreshed_turtle(self, turtle):
        # no need to do stuff
        pass

    def set_speed(self, speed):
        # the pillow canvas has no animation
        pass

    def exit_on_click(self):
        pass

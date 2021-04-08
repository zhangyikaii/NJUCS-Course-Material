"""The graphics module implements a simple GUI library."""

import sys
import math

try:
    import tkinter
except Exception as e:
    print('Could not load tkinter: ' + str(e))

FRAME_TIME = 1/30

class Canvas(object):
    """A Canvas object supports drawing and animation primitives.

    draw_* methods return the id number of a shape object in the underlying Tk
    object.  This id can be passed to move_* and edit_* methods.

    Canvas is a singleton; only one Canvas instance can be created.

    """

    _instance = None

    def __init__(self, width=1100, height=768, title='', color='White', tk=None):
        # Singleton enforcement
        if Canvas._instance is not None:
            raise Exception('Only one canvas can be instantiated.')
        Canvas._instance = self

        # Attributes
        self.color = color
        self.width = width
        self.height = height

        # Root window
        self._tk = tk or tkinter.Tk()
        self._tk.protocol('WM_DELETE_WINDOW', sys.exit)
        self._tk.title(title or 'Graphics Window')
        self._tk.bind('<Button-1>', self._click)
        self._click_pos = None

        # Canvas object
        self._canvas = tkinter.Canvas(self._tk, width=width, height=height)
        self._canvas.pack()
        self._draw_background()
        self._canvas.update()
        self._images = dict()

    def clear(self, shape='all'):
        """Clear all shapes, text, and images."""
        self._canvas.delete(shape)
        if shape == 'all':
            self._draw_background()
        self._canvas.update()

    def draw_polygon(self, points, color='Black', fill_color=None, filled=1, smooth=0, width=1):
        """Draw a polygon and return its tkinter id.

        points -- a list of (x, y) pairs encoding pixel positions
        """
        if fill_color == None:
            fill_color = color
        if filled == 0:
            fill_color = ""
        return self._canvas.create_polygon(flattened(points), outline=color, fill=fill_color,
                smooth=smooth, width=width)

    def draw_circle(self, center, radius, color='Black', fill_color=None, filled=1, width=1):
        """Draw a cirlce and return its tkinter id.

        center -- an (x, y) pair encoding a pixel position
        """
        if fill_color == None:
            fill_color = color
        if filled == 0:
            fill_color = ""
        x0, y0 = [c - radius for c in center]
        x1, y1 = [c + radius for c in center]
        return self._canvas.create_oval(x0, y0, x1, y1, outline=color, fill=fill_color, width=width)

    def draw_line(self, start, end, color='Blue', width=1):
        """Draw a line and return its tkinter id.

        start, end -- (x, y) pairs encoding a pixel position
        """
        x0, y0 = start
        x1, y1 = end
        return self._canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def draw_image(self, pos, image_file=None, scale=1, anchor=tkinter.NW, behind=0):
        """Draw an image from a file and return its tkinter id."""
        key = (image_file, scale)
        if key not in self._images:
            image = tkinter.PhotoImage(file=image_file)
            if scale >= 1:
                image = image.zoom(int(scale))
            else:
                image = image.subsample(int(1/scale))
            self._images[key] = image

        image = self._images[key]
        x, y = pos
        id = self._canvas.create_image(x, y, image=image, anchor=anchor)
        if behind > 0:
            self._canvas.tag_lower(id, behind)
        return id

    def draw_text(self, text, pos, color='Black', font='Arial',
                  size=12, style='normal', anchor=tkinter.NW):
        """Draw text and return its tkinter id."""
        x, y = pos
        font = (font, str(size), style)
        return self._canvas.create_text(x, y, fill=color, text=text, font=font, anchor=anchor)

    def edit_text(self, id, text=None, color=None, font=None, size=12,
                  style='normal'):
        """Edit the text, color, or font of an existing text object."""
        if color is not None:
            self._canvas.itemconfigure(id, fill=color)
        if text is not None:
            self._canvas.itemconfigure(id, text=text)
        if font is not None:
            self._canvas.itemconfigure(id, font=(font, str(size), style))

    def animate_shape(self, id, duration, points_fn, frame_count=0):
        """Animate an existing shape over points."""
        max_frames = duration // FRAME_TIME
        points = points_fn(frame_count)
        self._canvas.coords(id, flattened(points))
        if frame_count < max_frames:
            def tail():
                """Continues the animation at the next frame."""
                self.animate_shape(id, duration, points_fn, frame_count + 1)
            self._tk.after(int(FRAME_TIME * 1000), tail)

    def slide_shape(self, id, end_pos, duration, elapsed=0):
        """Slide an existing shape to end_pos."""
        points = paired(self._canvas.coords(id))
        start_pos = points[0]
        max_frames = duration // FRAME_TIME
        def points_fn(frame_count):
            completed = frame_count / max_frames
            offset = [(e - s) * completed for s, e in zip(start_pos, end_pos)]
            return [shift_point(p, offset) for p in points]
        self.animate_shape(id, duration, points_fn)

    def wait_for_click(self, seconds=0):
        """Return (position, elapsed) pair of click position and elapsed time.

        position: (x,y) pixel position of click
        elapsed:  milliseconds elapsed since call
        seconds:  maximum number of seconds to wait for a click

        If there is still no click after the given time, return (None, seconds).

        """
        elapsed = 0
        while elapsed < seconds or seconds == 0:
            if self._click_pos is not None:
                pos = self._click_pos
                self._click_pos = None
                return pos, elapsed
            self._sleep(FRAME_TIME)
            elapsed += FRAME_TIME
        return None, elapsed

    def _draw_background(self):
        w, h = self.width - 1, self.height - 1
        corners = [(0,0), (0, h), (w, h), (w, 0)]
        self.draw_polygon(corners, self.color, fill_color=self.color, filled=True, smooth=False)

    def _click(self, event):
        self._click_pos = (event.x, event.y)

    def _sleep(self, seconds):
        self._tk.update_idletasks()
        self._tk.after(int(1000 * seconds), self._tk.quit)
        self._tk.mainloop()

def flattened(points):
    """Return a flat list of coordinates from a list of pairs."""
    coords = list()
    [coords.extend(p) for p in points]
    return tuple(coords)

def paired(coords):
    """Return a list of pairs from a flat list of coordinates."""
    assert len(coords) % 2 == 0, 'Coordinates are not paired.'
    points = []
    x = None
    for elem in coords:
        if x is None:
            x = elem
        else:
            points.append((x, elem))
            x = None
    return points

def translate_point(point, angle, distance):
    """Translate a point a distance in a direction (angle)."""
    x, y = point
    return (x + math.cos(angle) * distance, y + math.sin(angle) * distance)

def shift_point(point, offset):
    """Shift a point by an offset."""
    x, y = point
    dx, dy = offset
    return (x + dx, y + dy)

def rectangle_points(pos, width, height):
    """Return the points of a rectangle starting at pos."""
    x1, y1 = pos
    x2, y2 = width + x1, height + y1
    return [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

def format_color(r, g, b):
    """Format a color as a string.

    r, g, b -- integers from 0 to 255
    """
    return '#{0:02x}{1:02x}{2:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
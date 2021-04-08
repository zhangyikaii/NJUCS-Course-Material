
from .canvas import Canvas

def _forward(method):
    def func(self, *args, **kwargs):
        # pylint: disable=W0212
        return getattr(self._canvas, method)(*args, **kwargs)
    func.name = method
    return func

class ForwardingCanvas(Canvas):
    """
    Canvas that dispatches all calls to a contained canvas
    """
    def __init__(self, canvas):
        super().__init__(canvas.width, canvas.height)
        self._canvas = canvas

    @property
    def turtle(self):
        return self._canvas.turtle

    @turtle.setter
    def turtle(self, turtle):
        self._canvas.turtle = turtle

    def set_canvas(self, canvas):
        canvas.turtle = self._canvas.turtle
        self._canvas = canvas
        self.width = canvas.width
        self.height = canvas.height

    draw_rectangular_line = _forward("draw_rectangular_line")
    draw_circle = _forward("draw_circle")
    fill_path = _forward("fill_path")
    axis_aligned_rectangle = _forward("axis_aligned_rectangle")
    set_bgcolor = _forward("set_bgcolor")
    clear = _forward("clear")
    refreshed_turtle = _forward("refreshed_turtle")
    set_speed = _forward("set_speed")
    exit_on_click = _forward("exit_on_click")

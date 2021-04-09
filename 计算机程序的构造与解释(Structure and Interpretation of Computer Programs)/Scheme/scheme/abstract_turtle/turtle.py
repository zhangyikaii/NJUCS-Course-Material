
from .forwarding_canvas import ForwardingCanvas
from .logging_canvas import LoggingCanvas
from .turtle_class import Turtle

__canvas = ForwardingCanvas(LoggingCanvas(1000, 1000))
__turtle = Turtle(__canvas)

for method_name in dir(__turtle):
    method = getattr(__turtle, method_name)
    if getattr(method, "is_turtle_method", False):
        globals()[method_name] = method

def set_canvas(canvas):
    __canvas.set_canvas(canvas)

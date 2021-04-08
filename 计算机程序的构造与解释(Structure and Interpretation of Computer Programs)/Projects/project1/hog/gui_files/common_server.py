import argparse
import json
import socketserver
import ssl
import traceback
import webbrowser
import os
from http import HTTPStatus, server
from http.server import HTTPServer
from urllib.parse import unquote
from urllib.request import Request, urlopen

PATHS = {}


def route(path):
    """Register a route handler."""

    if callable(path):
        return route("/" + path.__name__)(path)

    def wrap(f):
        PATHS[path] = f
        return f

    return wrap


class Handler(server.BaseHTTPRequestHandler):
    """HTTP handler."""

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        path = GUI_FOLDER + unquote(self.path)[1:]
        if "scripts" in path and not path.endswith(".js"):
            path += ".js"

        if path.endswith(".css"):
            self.send_header("Content-type", "text/css")
        elif path.endswith(".js"):
            self.send_header("Content-type", "application/javascript")
        self.end_headers()
        if path == GUI_FOLDER:
            path = GUI_FOLDER + "index.html"
        try:
            with open(path, "rb") as f:
                self.wfile.write(f.read())
        except Exception as e:
            print(e)
            # raise

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        raw_data = self.rfile.read(content_length).decode("utf-8")
        data = json.loads(raw_data)
        path = unquote(self.path)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        try:
            result = PATHS[path](**snakify(data))
            self.wfile.write(bytes(json.dumps(result), "utf-8"))
        except Exception as e:
            print(e)
            raise

    def log_message(self, *args, **kwargs):
        pass


def multiplayer_post(path, data, server_url=None):
    """Post DATA to a multiplayer server PATH and return the response."""
    if not server_url:
        server_url = DEFAULT_SERVER
    data_bytes = bytes(json.dumps(data), encoding="utf-8")
    request = Request(server_url + path, data_bytes, method="POST")
    try:
        response = urlopen(request, context=ssl._create_unverified_context())
        text = response.read().decode("utf-8")
        if text.strip():
            return json.loads(text)
    except Exception as e:
        traceback.print_exc()
        print(e)
        return None


def multiplayer_route(path, server_path=None):
    """Convert a function that takes (data, send) into a route."""
    if not server_path:
        server_path = path

    def wrap(f):
        def send(data):
            return multiplayer_post(server_path, data)

        def routed_fn(data):
            response = f(data, send)
            return response

        route(path)(routed_fn)
        return f

    return wrap


def forward_to_server(data, send):
    """Forward a request to the multiplayer server."""
    return send(data)


def start_server():
    global IS_SERVER
    IS_SERVER = True
    from flask import Flask, request, jsonify, send_from_directory

    app = Flask(__name__, static_url_path="", static_folder="")
    for route, handler in PATHS.items():

        def wrapped_handler(handler=handler):
            return jsonify(handler(**snakify(request.get_json(force=True))))

        app.add_url_rule(route, handler.__name__, wrapped_handler, methods=["POST"])

    @app.route("/")
    def index():
        return send_from_directory("", "index.html")

    return app


def start_client(port, default_server, gui_folder, standalone):
    """Start web server."""
    global DEFAULT_SERVER, GUI_FOLDER, IS_SERVER
    DEFAULT_SERVER = default_server
    GUI_FOLDER = gui_folder
    IS_SERVER = False

    socketserver.TCPServer.allow_reuse_address = True
    httpd = HTTPServer(("localhost", port), Handler)
    if not standalone:
        webbrowser.open("http://localhost:" + str(port), new=0, autoraise=True)
    httpd.serve_forever()


def snakify(data):
    out = {}
    for key, val in data.items():
        snake_key = []
        for x in key:
            if x == x.upper():
                snake_key += "_"
            snake_key += x.lower()
        out["".join(snake_key)] = val
    return out


def start(port, default_server, gui_folder):
    parser = argparse.ArgumentParser(description="Project GUI Server")
    parser.add_argument(
        "-s", help="Stand-alone: do not open browser", action="store_true"
    )
    parser.add_argument("-f", help="Force Flask app", action="store_true")
    args, unknown = parser.parse_known_args()

    import __main__

    if "gunicorn" not in os.environ.get("SERVER_SOFTWARE", "") and not args.f:
        start_client(port, default_server, gui_folder, args.s)
    else:
        app = start_server()
        if args.f:
            app.run(port=port, threaded=False)
        else:
            return app

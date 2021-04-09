import os
import time
from _socket import timeout
from http import server
import io
import json
import socketserver
import subprocess
import sys
import urllib.parse
import webbrowser
import threading
from http import HTTPStatus
from urllib.error import URLError
from urllib.request import Request, urlopen

import execution
import ok_interface
import log
from documentation import search
from execution_parser import strip_comments
from file_manager import get_scm_files, save, read_file, new_file
from formatter import prettify
from persistence import save_config, load_config
from runtime_limiter import TimeLimitException, OperationCanceledException, scheme_limiter
from scheme_exceptions import SchemeError, ParseError, TerminatedError

PORT = 8012

main_files = []

state = {}


class Handler(server.BaseHTTPRequestHandler):
    cancellation_event = threading.Event()  # Shared across all instances, because the threading mixin creates a new instance every time...

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        raw_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(raw_data.decode("ascii"))
        path = urllib.parse.unquote(self.path)
        result = self.handle_post_thread(data, path)
        return result

    def handle_post_thread(self, data, path):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/JSON")
        self.end_headers()

        if "code[]" not in data:
            data["code[]"] = [""]

        if path == "/cancel":
            self.cancellation_event.set()

        if path == "/process2":
            self.cancellation_event.clear()  # Make sure we don't have lingering cancellation requests from before
            code = data["code[]"]
            curr_i = int(data["curr_i"][0])
            curr_f = int(data["curr_f"][0])
            global_frame_id = int(data["globalFrameID"][0])
            visualize_tail_calls = data["tailViz"][0] == "true"
            self.wfile.write(bytes(handle(code, curr_i, curr_f, global_frame_id, visualize_tail_calls,
                                          cancellation_event=self.cancellation_event),
                                   "utf-8"))

        elif path == "/save":
            code = data["code[]"]
            filename = data["filename"][0]
            do_save = data["do_save"][0] == "true"
            if do_save:
                save(code, filename)
            self.wfile.write(bytes(json.dumps({"result": "success", "stripped": strip_comments(code)}), "utf-8"))

        elif path == "/instant":
            code = data["code[]"]
            global_frame_id = int(data["globalFrameID"][0])
            self.wfile.write(bytes(instant(code, global_frame_id), "utf-8"))

        elif path == "/reformat":
            code = data["code[]"]
            javastyle = data["javastyle"][0] == "true"
            self.wfile.write(bytes(json.dumps({"result": "success", "formatted": prettify(code, javastyle)}), "utf-8"))

        elif path == "/test":
            self.cancellation_event.clear()  # Make sure we don't have lingering cancellation requests from before
            output = cancelable_subprocess_call(self.cancellation_event, (sys.argv[0], os.path.splitext(ok_interface.__file__)[0] + ".py"), -1, sys.executable, subprocess.PIPE, subprocess.PIPE, None)
            self.wfile.write(output.split(ok_interface.BEGIN_OUTPUT)[1])

        elif path == "/list_files":
            self.wfile.write(bytes(json.dumps(get_scm_files()), "utf-8"))

        elif path == "/read_file":
            filename = data["filename"][0]
            self.wfile.write(bytes(json.dumps(read_file(filename)), "utf-8"))

        elif path == "/new_file":
            filename = data["filename"][0]
            self.wfile.write(bytes(json.dumps({"success": new_file(filename)}), "utf-8"))

        elif path == "/save_state":
            global state
            for key, val in json.loads(data["state"][0]).items():
                if key == "states":
                    if "states" not in state:
                        state["states"] = val
                    else:
                        merge(state["states"], val)
                else:
                    state[key] = val
            if "settings" in state:
                save_config("settings", state["settings"])

        elif path == "/load_state":
            if "states" not in state:
                self.wfile.write(b"fail")
            else:
                self.wfile.write(bytes(json.dumps(state), "utf-8"))

        elif path == "/load_settings":
            try:
                if "settings" not in state:
                    state["settings"] = {}
                for key, val in load_config("settings").items():
                    state["settings"][key] = val
            except FileNotFoundError:
                self.wfile.write(b"fail")
            else:
                self.wfile.write(bytes(json.dumps(state["settings"]), "utf-8"))


        elif path == "/documentation":
            query = data.get("query", [""])[0]
            self.wfile.write(bytes(json.dumps(search(query)), "utf-8"))

        elif path == "/kill":
            # This is (only) fine because we're in a different thread than the actual server
            self.server.shutdown()
            self.server.socket.close()

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        path = "editor/static/" + urllib.parse.unquote(self.path)[1:]

        if "scripts" in path and not path.endswith(".js"):
            path += ".js"

        if path.endswith(".css"):
            self.send_header("Content-type", "text/css")
        elif path.endswith(".js"):
            self.send_header("Content-type", "application/javascript")
        self.end_headers()
        if path == "editor/static/":
            path = "editor/static/index.html"
        try:
            with open(path, "rb") as f:  # lol better make sure that port is closed
                self.wfile.write(f.read()
                                 .replace(b"<START_DATA>",
                                          bytes(repr(json.dumps({"files": main_files})),
                                                "utf-8")))
        except Exception as e:
            print(e)
            # raise

    def log_message(self, *args, **kwargs):
        pass


def merge(states, new_states):
    for i, new_state in enumerate(new_states):
        if i == len(states):
            states.append(new_state)
        else:
            for key, val in new_state.items():
                states[i][key] = val


def cancelable_subprocess_call(cancellation_event, *args, **kwargs):
    buffered = io.BytesIO()
    with subprocess.Popen(*args, **kwargs) as proc:
        proc.stdin.close()
        def pipeline(source, *sinks):  # We need this extra thread because there's no cross-platform way to poll a process's stdout
            while True:
                s = source.readline()
                if not s: break
                for sink in sinks:
                    sink.write(s)
        reader_thread = threading.Thread(target=pipeline, args=(proc.stdout, buffered))
        reader_thread.daemon = True
        reader_thread.start()
        try:
          poll_interval = socketserver.BaseServer.serve_forever.__defaults__[0] / 8
          while proc.poll() is None:
              if cancellation_event.wait(poll_interval):
                  proc.terminate()
                  break
        finally:
            proc.terminate()  # Make sure subprocess is terminated no matter what (although it shouldn't be alive at this point)
            reader_thread.join()
    return buffered.getvalue()


def handle(code, curr_i, curr_f, global_frame_id, visualize_tail_calls, cancellation_event):

    try:
        global_frame = log.logger.frame_lookup.get(global_frame_id, None)
        log.logger.new_query(global_frame, curr_i, curr_f)
        scheme_limiter(cancellation_event,
                       execution.string_exec,
                       code, log.logger.out,
                       visualize_tail_calls,
                       global_frame.base if global_frame_id != -1 else None)
    except OperationCanceledException:
        return json.dumps({"success": False, "out": [str("operation was canceled")]})
    except ParseError as e:
        return json.dumps({"success": False, "out": [str(e)]})

    out = log.logger.export()
    return json.dumps(out)


def instant(code, global_frame_id):
    global_frame = log.logger.frame_lookup[global_frame_id]
    log.logger.new_query(global_frame)
    try:
        log.logger.preview_mode(True)
        scheme_limiter(0.3, execution.string_exec, code, log.logger.out, False, global_frame.base)
    except (SchemeError, ZeroDivisionError) as e:
        log.logger.out(e)
    except TimeLimitException:
        pass
    except Exception as e:
        raise
    finally:
        log.logger.preview_mode(False)
    return json.dumps({"success": True, "content": log.logger.export()["out"]})


# Source: https://stackoverflow.com/questions/7445658/how-to-detect-if-the-console-does-support-ansi-escape-codes-in-python
def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True


class ThreadedHTTPServer(socketserver.ThreadingMixIn, server.HTTPServer):
    daemon_threads = True


def start(file_args, port, open_browser):
    global main_files
    main_files = file_args
    global PORT
    PORT = port
    socketserver.TCPServer.allow_reuse_address = True

    e = None
    for port in range(PORT, PORT + 10):
        request = Request(f"http://127.0.0.1:{port}/kill", method='POST')
        try:
            urlopen(request, timeout=2)
            print("Killing existing editor process...")
            time.sleep(1)
        except (URLError, timeout):
            pass

        try:
            httpd = ThreadedHTTPServer(("127.0.0.1", port), Handler)
        except OSError as e:
            print(f"Port {port} is currently in use, trying a different port...")
        else:
            PORT = port
            url = f"http://127.0.0.1:{PORT}"
            break
    else:
        if supports_color():
            print("\033[91m", end="")
        print(f"Unable to connect to any candidate ports, printing debug information:")
        print(e)
        if supports_color():
            print("\033[0m", end="")
        return

    print(url)

    if open_browser:
        webbrowser.open(f"http://127.0.0.1:{PORT}", new=0, autoraise=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" - Ctrl+C pressed")
        print("Shutting down server - all unsaved work may be lost")
        print(
'''
      _____   _______    ____    _____  
     / ____| |__   __|  / __ \  |  __ \ 
    | (___      | |    | |  | | | |__) |
     \___ \     | |    | |  | | |  ___/ 
     ____) |    | |    | |__| | | |     
    |_____/     |_|     \____/  |_|     
''')
        if supports_color():
            print("\033[91m" + "\033[1m" + "\033[4m", end="")
        print("Remember that you should run python ok in a separate terminal window, to avoid stopping the editor process.")
        if supports_color():
            print("\033[0m" * 3, end="")

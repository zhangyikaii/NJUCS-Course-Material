import json

from flask import Flask, render_template, request, jsonify

import database
import execution
import log
from runtime_limiter import scheme_limiter, TimeLimitException
from scheme_exceptions import SchemeError

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", start_data=json.dumps({}))


@app.route("/<code>")
def lookup(code):
    val = database.load(code)
    if val is None:
        return index()
    return render_template("index.html",
                           start_data=repr(json.dumps({"code": eval(val[0]),
                                                       "skip_tree": bool(val[1]),
                                                       "hide_return_frames": bool(val[2])})))


@app.route("/process2", methods=["POST"])
def receive():
    code = request.form.getlist("code[]")
    skip_tree = request.form.get("skip_tree") == "true"
    skip_envs = request.form.get("skip_envs") == "true"
    hide_return_frames = request.form.get("hide_return_frames") == "true"
    return handle(code, skip_tree, skip_envs, hide_return_frames)


def handle(code, skip_tree, skip_envs, hide_return_frames):
    log.logger.setID(database.save(code, skip_tree, hide_return_frames))
    log.logger.new_query(skip_tree, skip_envs, hide_return_frames)
    try:
        # execution.string_exec(code, gui.logger.out)
        scheme_limiter(3, execution.string_exec, code, log.logger.out)
    except SchemeError as e:
        log.logger.out(e)
    except TimeLimitException:
        log.logger.out("Time limit exceeded. Try disabling the substitution visualizer (top checkbox) for increased "
                       "performance.")
    except Exception as e:
        log.logger.out(e)

    out = log.logger.export()
    return jsonify(out)


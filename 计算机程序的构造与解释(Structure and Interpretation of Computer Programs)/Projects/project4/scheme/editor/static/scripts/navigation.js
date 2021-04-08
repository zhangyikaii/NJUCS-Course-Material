import {saveState, states} from "./state_handler";
import {request_update} from "./event_handler";
import {get_i} from "./substitution_tree_worker";

export {init_events, get_curr_frame, get_active_node, go_to_end};

function fix_expr_i(i) {
    if (states[i].states[states[i].expr_i][0] <= states[i].index &&
        states[i].index < states[i].states[states[i].expr_i][1]) {
        return;
    }
    for (let expr_i = 0; expr_i !== states[i].states.length; ++expr_i) {
        if (states[i].states[expr_i][0] <= states[i].index &&
            states[i].index < states[i].states[expr_i][1]) {
            states[i].expr_i = expr_i;
            states[i].start = states[i].states[states[i].expr_i][0];
            states[i].end = states[i].states[states[i].expr_i][1];
        }
    }
}

// Largest i such that arr[i] < val
function closest_left(val, arr) {
    let low = 0;
    let high = arr.length;

    while (low + 1 < high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] >= val) {
            high = mid;
        } else {
            low = mid;
        }
    }

    return low;
}

// Smallest i such that arr[i] > val
function closest_right(val, arr) {
    return Math.min(arr.length - 1, closest_left(val, arr, false) + 1);
}

function next_frame_update(i) {
    states[i].index = states[i].frameUpdates[closest_right(states[i].index + 1, states[i].frameUpdates)];
    fix_expr_i(i);
    request_update();
}

function prev_frame_update(i) {
    states[i].index = states[i].frameUpdates[closest_left(states[i].index, states[i].frameUpdates)];
    fix_expr_i(i);
    request_update();
}

function next_expr(i) {
    states[i].expr_i = Math.min(states[i].expr_i + 1, states[i].states.length - 1);
    states[i].start = states[i].states[states[i].expr_i][0];
    states[i].end = states[i].states[states[i].expr_i][1];
    states[i].index = states[i].start;
    saveState();
    request_update();
}

function prev_expr(i) {
    states[i].expr_i = Math.max(states[i].expr_i - 1, 0);
    states[i].start = states[i].states[states[i].expr_i][0];
    states[i].end = states[i].states[states[i].expr_i][1];
    states[i].index = states[i].start;
    saveState();
    request_update();
}

function next_i(i) {
    states[i].index += 1;
    if (states[i].index === states[i].end && states[i].expr_i !== states[i].states.length - 1) {
        next_expr(i);
    } else {
        states[i].index = Math.min(states[i].index, states[i].end - 1);
    }
    saveState();
    request_update();
}

function prev_i(i) {
    states[i].index -= 1;
    if (states[i].index === states[i].start - 1 && states[i].expr_i !== 0) {
        prev_expr(i);
        states[i].index = states[i].end - 1;
    } else {
        states[i].index = Math.max(states[i].index, states[i].start);
    }
    saveState();
    request_update();
}

function get_curr_frame(environments, i) {
    let latestFrame;
    for (let frame of environments) {
        // frame is meaningless
        if (frame["bindings"].length === 0) {
            continue;
        }
        // frame is closed
        if (frame["bindings"][frame["bindings"].length - 1][0] < i) {
            continue;
        }
        // frame not yet open
        if (frame["bindings"][0][0] > i) {
            continue;
        }
        latestFrame = frame;
    }
    return latestFrame;
}

// Acts on the latest frame that is open
function skip_frame(i) {
    let latestFrame = get_curr_frame(states[i].environments, states[i].index);
    if (latestFrame === undefined) {
        return;
    }
    let newIndex = latestFrame["bindings"][latestFrame["bindings"].length - 1][0];
    if (states[i].index === newIndex) {
        next_frame_update(i);
    } else {
        states[i].index = newIndex;
    }
    fix_expr_i(i);
    request_update();
}

// Acts on the latest frame that is open
function restart_frame(i) {
    let latestFrame = get_curr_frame(states[i].environments, states[i].index);
    if (latestFrame === undefined) {
        return;
    }
    let newIndex = latestFrame["bindings"][0][0];
    if (states[i].index === newIndex) {
        prev_frame_update(i);
    } else {
        states[i].index = newIndex;
    }
    fix_expr_i(i);
    request_update();
}

function get_active_node(i, id_only) {
    let pos = get_i(states[i].states[states[i].expr_i][2],
        states[i].roots[states[i].expr_i],
        states[i].index);

    let next = pos;

    while (true) {
        for (let child of pos.children) {
            if (child["transition_type"] !== "UNEVALUATED") {
                next = child;
            }
        }
        if (next !== pos) {
            pos = next;
            continue;
        }
        break;
    }

    if (id_only) {
        return pos["id"];
    }

    return states[i].states[states[i].expr_i][2][pos["id"]];
}

function go_to_end(i) {
    states[i].index = states[i].states[states[i].states.length - 1][1] - 1;
    fix_expr_i(i);
    request_update();
}

function go_to_start(i) {
    states[i].index = states[i].states[0][0];
    fix_expr_i(i);
    request_update();
}

function finish_eval(i) {
    let node = get_active_node(i);
    console.log(node);
    let newIndex = node["transitions"][node["transitions"].length - 1][0];
    if (states[i].index >= newIndex || node["transitions"][node["transitions"].length - 1][1] !== "EVALUATED") {
        if (states[i].expr_i === states[i].states.length - 1) {
            go_to_end(i);
        } else {
            next_i(i);
        }
    } else {
        states[i].index = newIndex;
        fix_expr_i(i);
        request_update();
    }
}

function restart_eval(i) {
    console.log("restart_eval");
    let node = get_active_node(i);
    let newIndex = node["transitions"][0][0];
    if (states[i].index === newIndex) {
        prev_i(i);
    } else {
        states[i].index = newIndex;
        fix_expr_i(i);
        request_update();
    }
}

function init_events() {
    console.log("init events!");
    $("#body").on("click", ".prev", function (e) {
        prev_i($(e.target).data("id"));
    });

    $("#body").on("click", ".next", function (e) {
        console.log("Next!");
        next_i($(e.target).data("id"));
    });

    $("#body").on("click", ".prev-expr", function (e) {
        prev_expr($(e.target).data("id"));
    });

    $("#body").on("click", ".next-expr", function (e) {
        next_expr($(e.target).data("id"));
    });

    $("#body").on("click", ".next-update", function (e) {
        next_frame_update($(e.target).data("id"));
    });

    $("#body").on("click", ".prev-update", function (e) {
        prev_frame_update($(e.target).data("id"));
    });

    $("#body").on("click", ".skip-frame", function (e) {
        skip_frame($(e.target).data("id"));
    });

    $("#body").on("click", ".restart-frame", function (e) {
        restart_frame($(e.target).data("id"));
    });

    $("#body").on("click", ".finish-eval", function (e) {
        finish_eval($(e.target).data("id"));
    });

    $("#body").on("click", ".restart-eval", function (e) {
        restart_eval($(e.target).data("id"));
    });

    $("#body").on("click", ".go-to-end", function (e) {
        go_to_end($(e.target).data("id"));
    });

    $("#body").on("click", ".go-to-start", function (e) {
        go_to_start($(e.target).data("id"));
    });
}
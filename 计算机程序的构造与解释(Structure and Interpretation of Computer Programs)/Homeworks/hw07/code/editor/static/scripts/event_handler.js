import {notify_close, notify_open, open_prop} from "./layout";
import {saveState, states, temp_file} from "./state_handler";
import {register_cancel_button} from "./canceller";

export {request_update, request_reset, make, begin_slow, end_slow, init_complete, register}

const type_title = {
    "env_diagram": "Environments",
    "substitution_tree": "Debugger",
    "output": "Output",
    "test_results": "Test Results",
    "turtle_graphics": "Turtle Graphics"
};

let layout;

function register(inp_layout) {
    layout = inp_layout;
}

function request_update() {
    layout.eventHub.emit("update");
}

function request_reset() {
    layout.eventHub.emit("reset");
}

function make(container, type, id) {
    let title;
    if (states[id].file_name.startsWith(temp_file)) {
        title = states[id].file_name.slice(temp_file.length);
    } else {
        title = states[id].file_name;
    }

    if (type !== "editor") {
        title = type_title[type] + " (" + title + ")";
    }

    if (type === "test_results") {
        title = type_title[type];
    }

    let color;
    let icon;
    if (type === "editor") {
        if (id < $.parseJSON(start_data)["files"].length) {
            color = "orange";
        } else if (states[id].file_name.startsWith(temp_file)) {
            color = "red";
        } else {
            color = "grey";
        }
        icon = "file-code";
    } else if (type === "test_results") {
        color = "red";
        icon = "vials";
    } else if (type === "output") {
        color = "red";
        icon = "align-justify";
    } else if (type === "substitution_tree") {
        color = "purple";
        icon = "bug";
    } else if (type === "env_diagram") {
        color = "blue";
        icon = "project-diagram";
    } else if (type === "turtle_graphics") {
        color = "green";
        icon = "paint-brush";
    }
    title = `<span style="color: ${color};" class="fa fa-${icon}" aria-hidden=\"true\"></span> ` + title;

    container.setTitle(title);

    container.on("open", function () {
        notify_open(type, container, id);
        if (!initializing) {
            setTimeout(saveState, 0);
        }
    });

    container.on("destroy", function () {
        notify_close(type, container, id);
        states[id][open_prop.get(type)] = false;
        setTimeout(saveState, 0);
    });

    layout.eventHub.on("update", (e) => {
        if (states[id].up_to_date) {
            container.getElement().find(".output-warning").hide();
        } else {
            container.getElement().find(".output-warning").show();
        }
    });

    setTimeout(function () { $('[data-toggle="tooltip"]').tooltip({
        trigger: "hover"
    }); }, 0);
}

let timer;

function begin_slow() {
    end_slow(); // just in case!
    timer = setTimeout(function() {
        $("#loadingModal").modal("show");
        $("#terminate_btn").text("Cannot be Terminated");
        register_cancel_button($("#terminate_btn"));
        timer = -1;
    }, 300);
}

function end_slow() {
    if (timer) {
        clearInterval(timer);
        timer = undefined;
    }
    $("#loadingModal").modal("hide");
}

let initializing = true;

function init_complete() {
    initializing = false;
}
import {begin_slow, end_slow} from "./event_handler";
import {getLayout, setLayout} from "./layout";
import {getAllSettings, setAllSettings} from "./settings";

export {states, temp_file, loadState, saveState, make_new_state};

let base_state = {
    states: {},
    environments: [],
    moves: {"path": [], "showTurtle": false},
    out: "",
    heap: {},
    frameUpdates: [],

    index: 0,
    expr_i: 0,

    start: 0,
    end: 0,
    roots: ["demo"],

    globalFrameID: -1,
    
    editor_open: false,
    sub_open: false,
    env_open: false,
    turtle_open: false,
    out_open: false,
    tests_open: false,

    active_code: "",
    up_to_date: false,

    test_results: undefined,

    file_name: "",
};

let skip_saves = ["states", "environments", "moves", "out", "heap", "frameUpdates"];

let states = [];
for (let file of $.parseJSON(start_data)["files"]) {
    states.push(make_new_state());
    states[states.length - 1].file_name = file;
}

let temp_file = "__";

function make_new_state() {
    return jQuery.extend(true, {}, base_state);
}

async function loadState() {
    begin_slow();
    await $.post("./load_state", {})
        .done(function (data) {
            end_slow();
            if (data !== "fail") {
                data = $.parseJSON(data);
                states = data.states;
                setLayout(data.layout);
                setAllSettings(data.settings);
                for (let i = 0; i !== states.length; ++i) {
                    states[i] = jQuery.extend({}, base_state, states[i]);
                }
            }
        });
}

let curr_saving = false;
async function saveState(full=false, layout=undefined) {
    if (curr_saving) {
        return;
    }
    begin_slow();
    curr_saving = true;
    if (layout === undefined) {
        layout = getLayout();
    }

    let temp = [];

    if (full) {
        temp = states;
    } else {
        for (let state of states) {
            temp.push(jQuery.extend({}, state)); // shallow copy
        }

        for (let state of temp) {
            for (let key of skip_saves) {
                delete state[key];
            }
        }
    }

    await $.post("./save_state", {
        state: JSON.stringify({states: temp, layout: layout, settings: getAllSettings()}),
    }).done(function () {
        curr_saving = false;
        end_slow();
    });
}

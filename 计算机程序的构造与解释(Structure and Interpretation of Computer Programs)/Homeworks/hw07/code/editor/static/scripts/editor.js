import {saveState, states, temp_file} from "./state_handler";

import {open} from "./layout";
import {make, request_reset, request_update} from "./event_handler";
import {terminable_command} from "./canceller";
import {registerEditor, removeEditor, notify_changed} from "./test_results";
import {doTailViz, javastyle} from "./settings";

export {register};

function register(layout) {
    layout.registerComponent('editor', function (container, componentState) {
        let decoded = $.parseJSON(start_data);
        let testable = componentState.id < decoded["files"].length;
        let test_case = states[componentState.id].file_name.startsWith(temp_file);

        container.getElement().html(`
        <div class="content">
            <div class="header">        
                ${(!test_case) ?
            `<button type="button" class="btn-light save-btn" aria-label="Save">
                    <span class="text"> Save </span>
                </button>` : ``}


                <button type="button" data-toggle="tooltip"
                            title="Open a console and run the program locally."
                            class="btn-success toolbar-btn run-btn">Run</button>
                ${testable ?
            `<button type="button" data-toggle="tooltip"
                            title="Run all ok.py tests locally."
                            class="btn-danger toolbar-btn test-btn">Test</button>` : ``}
                <button type="button" data-toggle="tooltip"
                            title="Step through the program's execution."
                            class="btn-primary toolbar-btn sub-btn">Debug</button>          
                <button type="button" data-toggle="tooltip"
                            title="View environment diagram."
                            class="btn-info toolbar-btn env-btn">Environments</button>          
                <button type="button" data-toggle="tooltip"
                            title="Reformat code and fix (some) minor mistakes."
                            class="btn-secondary toolbar-btn reformat-btn">Reformat</button>          
            </div>
            <div class="editor-wrapper">
                <div class="editor"></div>
            </div>
        </div>
    `);

        make(container, "editor", componentState.id);

        let editorDiv;
        let editor;

        let changed = false;
        let saveTimer;

        let name;

        container.on("open", function () {
            editorDiv = container.getElement().find(".editor").get(0);
            editor = ace.edit(editorDiv);
            ace.config.set("packaged", true);
            editor.session.setMode("ace/mode/scheme");
            editor.setOption("fontSize", 14);
            editor.setOption("enableBasicAutocompletion", true);
            editor.setOption("enableLiveAutocompletion", true);
            editor.setAutoScrollEditorIntoView(true);
            editor.getSession().setUseSoftTabs(true);
            editor.container.style.background = "white";
            editor.focus();

            saveTimer = setInterval(() => save(), 5000);

            states[componentState.id].editor_open = true;

            container.on("resize", function () {
                editor.resize();
            });

            if (testable) {
                states[componentState.id].file_name = decoded["files"][componentState.id];
            }

            name = states[componentState.id].file_name;

            if (test_case) {
                editor.setValue(states[componentState.id].file_content);
                registerEditor(name, editor);
            } else {
                $.post("/read_file", {
                    filename: states[componentState.id].file_name,
                }).done(function (data) {
                    data = $.parseJSON(data);
                    editor.setValue(data);
                });
            }

            editor.getSession().on("change", function () {
                container.getElement().find(".save-btn > .text").text("Save");
                changed = true;
            });

            let selectMarker;

            function getMatchingBracket() {
                let cursor = editor.getCursorPosition();
                let index = editor.getSession().getDocument().positionToIndex(cursor);
                let nextVal = editor.getValue()[index];
                let prevVal = editor.getValue()[index - 1];

                if (prevVal === ")" || prevVal === "]") {
                    return editor.getSession().findMatchingBracket(cursor, prevVal);
                } else if (nextVal === "(" || nextVal === "[") {
                    cursor.column += 1;
                    let out = editor.getSession().findMatchingBracket(cursor, nextVal);
                    if (out !== null) {
                        out.column += 1;
                    }
                    return out;
                }
                return null;
            }

            editor.getSelection().on("changeCursor", function () {
                let matchingBracket = getMatchingBracket();
                if (selectMarker !== undefined) {
                    editor.getSession().removeMarker(selectMarker);
                }
                if (matchingBracket !== null) {
                    let currentPos = editor.getCursorPosition();

                    if (currentPos.row > matchingBracket.row ||
                        currentPos.row === matchingBracket.row && currentPos.column > matchingBracket.column) {
                        let temp = currentPos;
                        currentPos = matchingBracket;
                        matchingBracket = temp;
                    }

                    let range = new ace.Range(currentPos.row, currentPos.column, matchingBracket.row, matchingBracket.column);
                    selectMarker = editor.getSession().addMarker(range, "ace_selection match_parens", editor.getSelectionStyle());
                }
            });
        });

        layout.eventHub.on("update", () => {
            if (states[componentState.id].environments.length === 0) {
                // program has never been run
                container.getElement().find(".env-btn")//.prop("disabled", true)
                    .attr('data-original-title', "To use the environment diagram, press Run first.");
                container.getElement().find(".sub-btn")//.prop("disabled", true)
                    .attr('data-original-title', "To use the debugger, press Run first.");
            } else {
                container.getElement().find(".env-btn")//.prop("disabled", false)
                    .attr('data-original-title', "View environment diagram.");
                container.getElement().find(".sub-btn")//.prop("disabled", false)
                    .attr('data-original-title', "Step through the program's execution.");
            }
        });

        container.on("destroy", function () {
            removeEditor(name, editor);
            clearInterval(saveTimer);
        });


        container.getElement().keydown(function (event) {
            if ((event.ctrlKey || event.metaKey) && event.keyCode === 13) {
                event.preventDefault();
                // noinspection JSIgnoredPromiseFromCall
                run();
            }
            if ((event.ctrlKey || event.metaKey) && event.keyCode === 83) {
                event.preventDefault();
                // noinspection JSIgnoredPromiseFromCall
                save();
            }
        });

        container.getElement().find(".run-btn").on("click", () => run());

        container.getElement().find(".save-btn").on("click", () => save());

        container.getElement().find(".reformat-btn").on("click", reformat);

        container.getElement().find(".sub-btn").on("click", async function () {
            await save();
            await run(true);
            open("substitution_tree", componentState.id);
        });

        container.getElement().find(".env-btn").on("click", async function () {
            await save();
            await run(true);
            open("env_diagram", componentState.id);
        });

        container.getElement().find(".test-btn").on("click", run_tests);

        async function save(running) {
            if (!running && !changed) {
                return;
            }

            if (test_case) {
                states[componentState.id].file_content = editor.getValue();
            }

            container.getElement().find(".save-btn > .text").text("Saving...");

            let code = [editor.getValue()];
            await $.post("./save", {
                code: code,
                filename: name,
                do_save: !test_case,
            }).done(function (data) {
                data = $.parseJSON(data);
                if (data["result"] === "success") {
                    container.getElement().find(".save-btn > .text").text("Saved");
                    changed = false;
                    if (running) {
                        states[componentState.id].active_code = data["stripped"];
                        states[componentState.id].up_to_date = true;
                        return;
                    }
                    if (states[componentState.id].active_code === data["stripped"]) {
                        if (!states[componentState.id].up_to_date) {
                            states[componentState.id].up_to_date = true;
                            request_update();
                        }
                        states[componentState.id].up_to_date = true;
                    } else {
                        states[componentState.id].up_to_date = false;
                    }
                } else {
                    alert("Save error - try copying code from editor to a file manually");
                }
            })
        }

        async function run(noOutput) {
            let code = [editor.getValue()];

            async function run_done(data) {
                data = $.parseJSON(data);
                if (data.success) {
                    states[componentState.id].states = data.states;
                    states[componentState.id].environments = [];
                    for (let key of data.active_frames) {
                        states[componentState.id].environments.push(data.frame_lookup[key]);
                    }
                    states[componentState.id].moves = data.graphics;
                    states[componentState.id].out = data.out[0];
                    states[componentState.id].start = data.states[0][0];
                    states[componentState.id].end = data.states[0][1];
                    states[componentState.id].index = data.states[0][0];
                    states[componentState.id].expr_i = 0;
                    states[componentState.id].roots = data.roots;
                    states[componentState.id].globalFrameID = data.globalFrameID;
                    states[componentState.id].heap = data.heap;
                    states[componentState.id].frameUpdates = data.frameUpdates;
                } else {
                    states[componentState.id].out = data.out[0];
                    states[componentState.id].globalFrameID = -1;
                }

                await save(true);

                if (!noOutput) {
                    open("output", componentState.id);
                    if (data.graphics_open) {
                        open("turtle_graphics", componentState.id);
                    }
                }
                // noinspection JSIgnoredPromiseFromCall
                saveState(true);
                request_reset();
                request_update();
            }

            let aj = $.post("./process2", {
                code: code,
                globalFrameID: -1,
                curr_i: 0,
                curr_f: 0,
                tailViz: doTailViz()
            });
            terminable_command("executing code", aj, run_done);
        }

        function reformat() {
            let code = [editor.getValue()];
            $.post("./reformat", {
                code: code,
                javastyle: javastyle(),
            }).done(function (data) {
                if (data) {
                    data = $.parseJSON(data);
                    editor.setValue(data["formatted"] + "\n");
                } else {
                    $("#formatFailModal").modal("show");
                }
            });
        }

        async function run_tests() {
            if (editor.getValue().trim() === "") {
                return;
            }
            await save();
            let ajax = $.post("./test");

            async function done_fn(data) {
                data = $.parseJSON(data);
                states[0].test_results = data;
                await save();
                notify_changed();
                open("test_results", 0);
            }

            terminable_command("test cases", ajax, done_fn);
        }
    });
}

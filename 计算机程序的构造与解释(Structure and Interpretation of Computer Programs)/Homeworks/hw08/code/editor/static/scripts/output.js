import {saveState, states} from "./state_handler";
import {make, request_update} from "./event_handler";
import {terminable_command} from "./canceller";
import {open} from "./layout";
import {display_elem} from "./env_diagram_worker";
import {go_to_end} from "./navigation";
import {doTailViz} from "./settings";

export {register};

let entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;'
};

let FUNCTIONS = new Map();

function escapeHtml(string) {
  return String(string).replace(/[&<>"'`=\/]/g, function (s) {
    return entityMap[s];
  });
}

FUNCTIONS.set("AUTODRAW", (i, id, outputDiv, componentState) => {
    if (componentState.autoDraw) {
        drawPair(i, id, outputDiv, componentState);
    }
});

FUNCTIONS.set("DRAW", drawPair);

FUNCTIONS.set("ENABLE_AUTODRAW", (outputDiv, componentState) => {
    componentState.autoDraw = true;
});

FUNCTIONS.set("DISABLE_AUTODRAW", (outputDiv, componentState) => {
    componentState.autoDraw = false;
});


function drawPair(i, id, outputDiv, componentState) {
    let rawSVG = document.createElement("svg");
    let svg = SVG(rawSVG);
    outputDiv.append(rawSVG);
    display_elem(0, 10,
        id,
        states[componentState.id].heap,
        svg,
        0,
        new Map(),
        i,
    );
    rawSVG.children[0].setAttribute("height", svg.bbox().h + 20);
}

function register(myLayout) {
    myLayout.registerComponent('output', function (container, componentState) {
        container.getElement().html(`
        <div class="output-warning">This session may be out of date! Hit "Run" to refresh contents.</div>
        <div class="output-wrapper">
            <div class="output-holder">
                <div class="output">[click Run to start!]</div>
            </div>
            <div class="console-wrapper">
                <div class="console-input"></div>
            </div>
            <div class="preview"></div>
        </div>
        `);

        make(container, "output", componentState.id);

        let preview = "";
        let editorDiv;
        let editor;

        let history = [""];
        let i = 0;

        function updatePreview() {
              container.getElement().find(".preview").html("<i>" + escapeHtml(preview) + "</i>");
        }

        myLayout.eventHub.on("update", function () {
            if (editorDiv) {
                if (states[componentState.id].globalFrameID === -1) {
                    $(editorDiv).hide();
                    editor.setValue("");
                } else {
                    $(editorDiv).show();
                }
            }

            container.getElement().find(".output").html(escapeHtml(states[componentState.id].out.trim()));
            let output = states[componentState.id].out.trim().split("\n");
            let outputDiv = container.getElement().find(".output");
            outputDiv.html("");
            componentState.autoDraw = false;
            for (let line of output) {
                let ok = false;
                for (let key of FUNCTIONS.keys()) {
                    if (line.startsWith(key)) {
                        let decoded = $.parseJSON(line.slice(key.length));
                        FUNCTIONS.get(key)(...decoded, outputDiv, componentState);
                        ok = true;
                        break;
                    }
                }
                if (!ok) {
                    outputDiv.append(escapeHtml(line + "\n"));
                }
            }

            updatePreview();
            container.getElement().find(".output-wrapper").scrollTop(
            container.getElement().find(".output-wrapper")[0].scrollHeight);
        });

        container.getElement().on("click", function () {
            setTimeout(() => {
                if (window.getSelection().rangeCount === 0 ||
                    window.getSelection().getRangeAt(0).collapsed) {
                    editor.focus();
                }
            }, 0);
        });

        container.on("open", function () {
            editorDiv = container.getElement().find(".console-input").get(0);
            editor = ace.edit(editorDiv);
            ace.config.set("packaged", true);
            editor.session.setMode("ace/mode/scheme");
            editor.setOption("fontSize", 14);
            editor.setOption("enableBasicAutocompletion", true);
            editor.setOption("minLines", 1);
            editor.setOption("maxLines", 100);
            editor.setOption("highlightActiveLine", false);
            editor.container.style.background = "white";
            editor.session.gutterRenderer = {
                getWidth: function (session, lastLineNumber, config) {
                    return 3 * config.characterWidth;
                },
                getText: function () {
                    return "scm> ";
                }
            };
            editor.focus();

            container.on("resize", function () {
                editor.resize();
            });

            editor.getSession().on("change", function () {
                let val = editor.getValue();
                val = val.replace(/\r/g, "");
                if (val.trim()) {
                    history[i] = val.trim();
                }
                if (val.slice(-1) === "\n") {
                    enter_key_pressed(val);
                } else {
                    $.post("./instant", {
                        code: [editor.getValue()],
                        globalFrameID: states[componentState.id].globalFrameID,
                    }).done(function (data) {
                        preview = "";
                        if (!data) {
                            updatePreview();
                        }
                        data = $.parseJSON(data);
                        if (data.success) {
                            preview = data.content;
                        } else {
                            preview = "";
                        }
                        updatePreview();
                    })
                }
            });

            function enter_key_pressed(val) {
                val = val.trim();
                editor.setReadOnly(true);
                editor.setReadOnly(false);
                editor.setValue("", 0);
                editor.focus();
                setTimeout(function () {
                    editor.setValue("", 0);
                }, 10);
                i = history.length - 1;
                history[i] = val.trim();
                ++i;
                history.push("");
                let displayVal = val.replace(/\n/g, "\n.... ");
                states[componentState.id].out += "\nscm> " + displayVal;
                request_update();
                function run_done(data) {
                    // editor.setValue(val.slice(firstTerminator + 1));
                    data = $.parseJSON(data);
                    if (data.out[0].trim() !== "") {
                        states[componentState.id].out += "\n" + data.out[0].trim();
                    }
                    if (data.success) {
                        for (let key of data.active_frames) {
                            states[componentState.id].environments.push(data.frame_lookup[key]);
                        }
                        states[componentState.id].environments[0] =
                            data.frame_lookup[states[componentState.id].globalFrameID];
                        states[componentState.id].states.push(...data.states);
                        states[componentState.id].roots.push(...data.roots);
                        $.extend(states[componentState.id].heap, data.heap);
                        states[componentState.id].frameUpdates.push(...data.frameUpdates);
                        states[componentState.id].moves = data.graphics;

                        if (data.graphics_open) {
                            open("turtle_graphics", componentState.id);
                        }
                    }
                    go_to_end(componentState.id);
                    request_update();
                    saveState(true);
                }
                let aj = $.post("./process2", {
                    code: [val],
                    globalFrameID: states[componentState.id].globalFrameID,
                    curr_i: states[componentState.id].states.slice(-1)[0][1],
                    curr_f: states[componentState.id].environments.length,
                    tailViz: doTailViz(),
                });
                terminable_command("executing code", aj, run_done);
            }

            let old_up_arrow = editor.commands.commandKeyBinding.up;
            editor.commands.addCommand({
                name: "uparrow",
                bindKey: { win: "Up", mac: "Up" },
                exec: function(editor, ...rest) {
                    if (editor.getCursorPosition().row === 0) {
                        if (i > 0) {
                            --i;
                        }
                        editor.setValue(history[i]);
                        editor.selection.clearSelection();
                     } else {
                        old_up_arrow.exec(editor, ...rest);
                    }
                },
            });

            editor.commands.addCommand({
                name: "ctrl-enter",
                bindKey: { win: "Ctrl+Enter", mac: "Cmd+Enter"},
                exec: function(editor, ...rest) {enter_key_pressed(editor.getValue().replace(/\r/g, ""));}
            });

            let old_down_arrow = editor.commands.commandKeyBinding.down;
            editor.commands.addCommand({
                name: "downarrow",
                bindKey: { win: "Down", mac: "Down" },
                exec: function(editor, ...rest) {
                    let numLines = editor.getSession().getLength();
                    if (editor.getCursorPosition().row === numLines - 1) {
                        if (i < history.length - 1) {
                            ++i;
                        }
                        editor.setValue(history[i]);
                        editor.selection.clearSelection();
                    } else {
                        old_down_arrow.exec(editor, ...rest);
                    }
                },
            });
        });

        container.on("shown", function () {
            request_update();
        })
    });
}

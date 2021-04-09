import {make_new_state, saveState, states, temp_file} from "./state_handler";
import {open} from "./layout";
import {make} from "./event_handler";

export {register, registerEditor, removeEditor, notify_changed};

let editors = new Map();

let up_to_date = true;

function notify_changed() {
    up_to_date = false;
}

function registerEditor(name, editor) {
    editors.set(name, editor);
}

function removeEditor(name) {
    editors.delete(name);
}

function register(myLayout) {
    myLayout.registerComponent('test_results', function (container, componentState) {
        if (componentState.id !== 0) {
            alert("Something went wrong with the okpy frontend. Try running the testcases from the console, and let the maintainer of this tool know what happened.")
        }
        myLayout.eventHub.on("update", function () {
            let data = states[0].test_results;
            container.getElement().html(`<div id="accordion"> </div>`);
            let expanded = false;
            for (let entry of data) {
                let random_id = Math.random().toString(36).replace(/[^a-z]+/g, '');
                let card_style = entry.passed ? "bg-success" : "bg-danger";
                let hideshow = (!expanded && !entry.passed) ? "show" : "hide";
                expanded |= !entry.passed;
                $("#accordion").append(`
                <div class="card">
                    <div class="card-header ${card_style} text-white" id="${random_id + "x"}" data-toggle="collapse" 
                    data-target="#${random_id}"> ${entry.problem} </div>
                    <div id="${random_id}" class="collapse ${hideshow}" aria-labelledby="${random_id + "x"}" data-parent="#accordion">
                    <div class="card-body" style="padding: 5px">
                        <table class="table table-sm table-hover">
                            <tbody>
                            </tbody>
                      </table>
                      </div>
                    </div>
                </div>
                `);

                for (let i = 0; i !== entry.suites.length; ++i) {
                    for (let j = 0; j !== entry.suites[i].length; ++j) {
                        let test = entry.suites[i][j];
                        let pass_string = (test.passed ? "Passed!" : "Failed!");
                        let class_string = (test.passed ? "" : "font-bold");
                        $("#accordion").children().last().find("tbody").append(`
                        <tr class="${class_string}">
                            <td class="align-middle">Suite ${i + 1}, Case ${j + 1}</td> 
                            <td class="align-middle">${pass_string}</td> 
                            <td class="text-right"> <button class="btn btn-secondary"> View Case </button> </td>
                        </tr>`);
                        let case_name = `${entry.problem} - Suite ${i + 1}, Case ${j + 1}`;
                        if (!up_to_date &&
                            editors.has(temp_file + case_name)) {
                            editors.get(temp_file + case_name).setValue(test.code);
                            for (let i = 0; i !== states.length; ++i) {
                                if (states[i].file_name === temp_file + case_name) {
                                    states[i].up_to_date = false;
                                    states[i].active_code = "fail";
                                    break;
                                }
                            }
                        }
                        $(`#${random_id}`).find(".btn").last().click(function () {
                            if (editors.has(temp_file + case_name)) {
                                for (let i = 0; i !== states.length; ++i) {
                                    if (states[i].file_name === temp_file + case_name) {
                                        open("editor", i);
                                        break;
                                    }
                                }
                            } else {
                                let index = states.length;
                                let new_state = make_new_state();
                                new_state.file_name = temp_file + case_name;
                                new_state.file_content = test.code;
                                states.push(new_state);
                                saveState();
                                open("editor", index);
                            }
                        });
                    }
                }
            }
            up_to_date = true;
        });

        make(container, "test_results", 0);
    });
}
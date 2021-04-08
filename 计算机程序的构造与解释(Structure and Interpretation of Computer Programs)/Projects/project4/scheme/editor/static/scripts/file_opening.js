import {make_new_state, saveState, states} from "./state_handler";
import {open} from "./layout";

export {init};

function init() {
    $("#new-btn").click(function () {
        $("#fileNameInput").val("");
        $("#newFileModal").modal();
        $("#file_already_exists").hide();
    });

    $("#newFileButton").click(
        async function () {
            let fileName = $("#fileNameInput").val();
            let success;
            await $.post("./new_file", {filename: $("#fileNameInput").val()}).done(function (data) {
                data = $.parseJSON(data);
                success = data["success"];
            });
            if (success) {
                $("#newFileModal").modal("hide");
                open_file(fileName + ".scm");
            } else {
                $("#file_already_exists").show().text(fileName + ".scm already exists.")
            }
        });

    $("#open-btn").click(function () {
        $.post("./list_files").done(function (data) {
            let files = new Set();
            for (let state of states) {
                if (state.editor_open) {
                    files.add(state.file_name);
                }
            }
            data = $.parseJSON(data);
            $("#fileChooserModal").modal();
            $("#file-list").html("");
            for (let file of data) {
                if (files.has(file)) {
                    $("#file-list").append(`
                    <tr><td class="align-middle">${file}</td> <td class="text-right"><button type="button" disabled class="btn btn-primary disabled">Already Open</button></td></tr>
                `);
                    continue;
                }
                $("#file-list").append(`
                        <tr>
                        <td class="align-middle">${file}</td> 
                        <td class="text-right">
                            <button type="button" class="btn btn-primary">Open</button>
                        </td>
                        </tr>
                    `);
                $("#file-list").children().last().find(".btn").click(function () {
                    open_file(file);
                    $("#fileChooserModal").modal("hide");
                });
            }
        })
    });
}

function open_file(file) {
    let index = states.length;
    let new_state = make_new_state();
    new_state.file_name = file;
    states.push(new_state);
    open("editor", index);
    // noinspection JSIgnoredPromiseFromCall
    saveState();
}
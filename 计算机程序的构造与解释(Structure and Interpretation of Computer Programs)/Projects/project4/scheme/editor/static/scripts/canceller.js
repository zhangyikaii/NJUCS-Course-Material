
import {begin_slow, end_slow} from "./event_handler";

export {register_cancel_button, terminable_command}

let has_command = false;
let command_description = undefined;

let button = undefined;

function register_cancel_button(btn) {
    button = btn;
    button.on("click", function() {
        console.log("on click");
        if (has_command) {
            $.post("./cancel", {});
            has_command = false;
            command_description = undefined;
        }
        refresh_button();
    });
    refresh_button();
}

function refresh_button() {
    if (button === undefined) {
        console.log("No button!");
        return;
    }
    if (has_command) {
        button.addClass('btn-danger');
        console.log(button);
        button.text("Terminate " + command_description);
    } else {
        button.removeClass('btn-danger');
    }
}

function terminable_command(label, ajax, done) {
    begin_slow();
    if (has_command) {
        throw Error("A command is already running");
    }
    function new_done(data) {
        end_slow();
        done(data);
        has_command = false;
        command_description = undefined;
        refresh_button();
    }
    has_command = true;
    command_description = label;

    refresh_button();
    ajax.done(new_done);
}

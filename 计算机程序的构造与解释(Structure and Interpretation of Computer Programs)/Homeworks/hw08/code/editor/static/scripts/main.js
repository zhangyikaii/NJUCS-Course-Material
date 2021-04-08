import * as navigation from "./navigation";
import * as layout from "./layout";
import * as file_opening from "./file_opening";
import * as settings from "./settings";
import * as documentation from "./documentation";
import * as keyboard_shortcuts from "./keyboard_shortcuts";
import {loadState} from "./state_handler";
import {end_slow, request_update} from "./event_handler";

$(window).on("load", async function () {
    await loadState();

    navigation.init_events();
    layout.init();
    file_opening.init();
    settings.init();
    documentation.init();
    keyboard_shortcuts.init();

    $(document).ajaxError(() => {
        end_slow();
        $("#disconnectedModal").modal("show");
    });

    request_update();
});
import * as env_diagram_worker from "./env_diagram_worker";
import {states} from "./state_handler";
import {make, request_update} from "./event_handler";

export { register };

function register(myLayout) {
    myLayout.registerComponent('env_diagram', function (container, componentState) {
        let random_id = Math.random().toString(36).replace(/[^a-z]+/g, '');
        container.getElement().html(`
        <div class="content">
        <div class="header">
            <div class="btn-toolbar bg-light">
                <button type="button" data-toggle="tooltip"
                        title="Step backward." data-id="${componentState.id}" 
                        class="btn btn-sm btn-light prev-update">
                        <i class="fas fa-arrow-left"></i>
                </button>          
                <button type="button" data-toggle="tooltip"
                        title="Step forward." data-id="${componentState.id}" 
                        class="btn btn-sm btn-light next-update">
                    <i class="fas fa-arrow-right"></i>
                </button>
                <button type="button" data-toggle="tooltip"
                        title="Go back to the opening of the frame." 
                        data-id="${componentState.id}" 
                        class="btn btn-sm btn-light restart-frame">
                    <i class="fas fa-angle-double-left"></i>
                </button>          
                <button type="button" data-toggle="tooltip"
                        title="Skip to the exit of the frame." 
                        data-id="${componentState.id}" 
                        class="btn btn-sm btn-light skip-frame">
                    <i class="fas fa-angle-double-right"></i>
                </button>          
                <button type="button" data-toggle="tooltip"
                        title="Go to the start of the program.." 
                        data-id="${componentState.id}" 
                        class="btn btn-sm btn-light go-to-start">
                    <i class="fas fa-arrow-alt-circle-left"></i>
                </button>          
                <button type="button" data-toggle="tooltip"
                        title="Finish executing the program." 
                        data-id="${componentState.id}" 
                        class="btn btn-sm btn-light go-to-end">
                    <i class="fas fa-arrow-alt-circle-right"></i>
                </button>
                <span data-toggle="tooltip" data-target="${random_id}"
                      title="Toggle box and pointer visualization.">
                    <div class="btn-group-toggle" data-toggle="buttons">
                      <label class="btn btn-sm btn-light" id="${random_id}">
                        <input type="checkbox" autocomplete="off" class="box-pointer-checkbox">
                        <i class="fas fa-th-large "></i>
                      </label>
                    </div>
                </span>
            </div>
            <div class="output-warning">
                This session may be out of date! Hit "Run" to refresh contents.
            </div>
        </div>
        <div class="envs">
            <svg></svg>
        </div>
        </div>
        `);

        make(container, "env_diagram", componentState.id);

        let rawSVG = container.getElement().find(".envs > svg").get(0);
        // svgPanZoom(rawSVG, {fit: false, zoomEnabled: true, center: false, controlIconsEnabled: true});
        let svg = SVG.adopt(rawSVG).size(container.width, container.height);

        let ready = false;

        myLayout.eventHub.on("update", function () {
            let zoom;
            let pan;

            if (ready) {
                zoom = svgPanZoom(rawSVG).getZoom();
                pan = svgPanZoom(rawSVG).getPan();
                svgPanZoom(rawSVG).destroy();
            }
            svg.clear();
            ready = true;
            // env_diagram_worker.display_env(states[componentState.id].environments, svg, states[componentState.id].index);
            env_diagram_worker.display_env_pointers(
                states[componentState.id].environments,
                states[componentState.id].heap,
                svg,
                states[componentState.id].index,
                states[componentState.id].start,
                container.getElement().find(".box-pointer-checkbox").is(":checked"),
                !states[componentState.id].up_to_date);
            svgPanZoom(rawSVG, {fit: false, zoomEnabled: true, center: false, controlIconsEnabled: true});
            if (isNaN(zoom)) {
                svgPanZoom(rawSVG).reset();
            } else {
                svgPanZoom(rawSVG).zoom(zoom);
                svgPanZoom(rawSVG).pan(pan);
            }
        });

        myLayout.eventHub.on("reset", function () {
            svgPanZoom(rawSVG).reset();
        });

        container.getElement().find(`#${random_id}`).on("click", function () {
            setTimeout(request_update, 0);
        });

        container.on("resize", function () {
            let zoom;
            let pan;

            if (ready) {
                zoom = svgPanZoom(rawSVG).getZoom();
                pan = svgPanZoom(rawSVG).getPan();
                svgPanZoom(rawSVG).destroy();
            }
            svg.size(container.width, container.height);
            svgPanZoom(rawSVG, {fit: false, zoomEnabled: true, center: false, controlIconsEnabled: true});
            if (isNaN(zoom)) {
                svgPanZoom(rawSVG).reset();
            } else {
                svgPanZoom(rawSVG).zoom(zoom);
                svgPanZoom(rawSVG).pan(pan);
            }

            ready = true;
        });

        container.on("shown", function () {
            request_update();
        })
    });
}
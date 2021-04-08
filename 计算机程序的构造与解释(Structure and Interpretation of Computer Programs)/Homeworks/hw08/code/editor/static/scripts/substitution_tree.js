import * as substitution_tree_worker from "./substitution_tree_worker"
import {
    make, request_update
} from "./event_handler";

export {
    register
};

function register(myLayout) {
    myLayout.registerComponent('substitution_tree', function (container, componentState) {
        let random_id = Math.random().toString(36).replace(/[^a-z]+/g, '');
        container.getElement().html(`
            <div class="content">
                <div class="header">
                <div class="btn-toolbar bg-light">
                    <button type="button" data-toggle="tooltip"
                            title="Step backward." data-id="${componentState.id}" 
                            class="btn btn-sm btn-light prev">
                            <i class="fas fa-arrow-left"></i>
                    </button>          
                    <button type="button" data-toggle="tooltip"
                            title="Step forward." data-id="${componentState.id}" 
                            class="btn btn-sm btn-light next">
                        <i class="fas fa-arrow-right"></i>
                    </button>
                    <button type="button" data-toggle="tooltip"
                            title="Go to the start of the evaluation of the current expression." 
                            data-id="${componentState.id}" 
                            class="btn btn-sm btn-light restart-eval">
                        <i class="fas fa-angle-double-left"></i>
                    </button>          
                    <button type="button" data-toggle="tooltip"
                            title="Finish evaluating the current expression." 
                            data-id="${componentState.id}" 
                            class="btn btn-sm btn-light finish-eval">
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
                          title="Toggle tree visualization.">
                        <div class="btn-group-toggle" data-toggle="buttons">
                          <label class="btn btn-sm btn-light" id="${random_id}">
                            <input type="checkbox" autocomplete="off" class="tree-checkbox">
                            <i class="fas fa-sitemap"></i>
                          </label>
                        </div>
                    </span>
                </div>
                <div class="output-warning">
                    This session may be out of date! Hit "Run" to refresh contents.
                </div>
                </div>
                <div class="tree">
                    <svg></svg>
                </div>
            </div>
        `);

        make(container, "substitution_tree", componentState.id);

        let rawSVG = container.getElement().find(".tree > svg").get(0);
        let svg = SVG.adopt(rawSVG).size(container.width, container.height);

        let ready = false;

        myLayout.eventHub.on("update", async () => {
            let zoom;
            let pan;

            let clearSVG = function () {
                if (ready) {
                    zoom = svgPanZoom(rawSVG).getZoom();
                    pan = svgPanZoom(rawSVG).getPan();
                    svgPanZoom(rawSVG).destroy();
                }
                ready = false;
            };

            await substitution_tree_worker.display_tree(componentState.id, svg, clearSVG,
                container.getElement().find(".tree-checkbox").is(":checked"));

            svgPanZoom(rawSVG, {
                fit: false,
                zoomEnabled: true,
                center: false,
                controlIconsEnabled: true
            });

            if (isNaN(zoom)) {
                svgPanZoom(rawSVG).reset();
            } else {
                svgPanZoom(rawSVG).zoom(zoom);
                svgPanZoom(rawSVG).pan(pan);
            }
            ready = true;
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
            ready = true;
            svgPanZoom(rawSVG, {
                fit: false,
                zoomEnabled: true,
                center: false,
                controlIconsEnabled: true
            });
            if (isNaN(zoom)) {
                svgPanZoom(rawSVG).reset();
            } else {
                svgPanZoom(rawSVG).zoom(zoom);
                svgPanZoom(rawSVG).pan(pan);
            }
        });
    });
}
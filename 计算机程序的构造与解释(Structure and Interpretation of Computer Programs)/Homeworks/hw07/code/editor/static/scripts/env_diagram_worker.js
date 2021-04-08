import {charWidth, charHeight} from "./measure";
import {hide_return_frames} from "./settings";
import {get_curr_frame} from "./navigation";

export {display_env_pointers, display_elem};

function display_env_pointers(environments, heap, container, i, start_i, pointers, vert_offset) {
    container.clear();

    let cache = new Map();

    let h = charHeight;

    let frame_data = [];
    let maxlen = 0;

    let active_frame = get_curr_frame(environments, i);
    let active_frame_data;

    for (let frame of environments) {
        let curr = [["", false]];
        let name_lookup = new Map();
        let k;
        for (k = 0; k !== frame["bindings"].length; ++k) {
            if (frame["bindings"][k][0] > i) {
                break;
            }
            if (hide_return_frames() &&
                ((frame["bindings"][k][1][0] === "Return Value" && frame["bindings"][k][0] < i)
                    || (frame !== environments[0] && frame["bindings"][k][0] < start_i))) {
                k = 0;
                break;
            }
            let line = "   " + frame["bindings"][k][1][0];
            let data = frame["bindings"][k][2];
            if (pointers && data[0]) {
                // non-atomic
            } else {
                line += ": " + frame["bindings"][k][1][1];
                data = false;
            }

            if (name_lookup.has(frame["bindings"][k][1][0])) {
                curr[name_lookup.get(frame["bindings"][k][1][0])] = [line, data];
            } else {
                name_lookup.set(frame["bindings"][k][1][0], curr.length);
                curr.push([line, data]);
            }
            maxlen = Math.max(maxlen, line.length);
        }
        if (k === 0) {
            continue;
        }
        let title = frame.name + ": " + frame.label;
        if (frame.parent !== "Global" && frame.name !== "Global") {
            title += " [parent = " + frame.parent + "]";
        }
        title += "\n";
        maxlen = Math.max(maxlen, title.length);
        curr[0] = [title, false];
        frame_data.push(curr);

        if (frame === active_frame) {
            active_frame_data = curr;
        }
    }

    maxlen += 5;

    let curr_y = 10 + vert_offset * 25;

    for (let frame of frame_data) {
        for (let k = 1; k < frame.length; ++k) {
            container.text(frame[k][0]).font("family", "Monaco, monospace").font("size", 14).dx(35).dy(curr_y + charHeight * k);
            if (frame[k][1]) {
                let is_box = (heap[frame[k][1][1]].length > 1);
                let valid = !cache.has(frame[k][1][1]);
                let depth = display_elem(
                    maxlen * charWidth + 45,
                    h + (is_box ? charHeight / 2 : 0),
                    frame[k][1],
                    heap,
                    container,
                    0,
                    cache,
                    i,
                    maxlen * charWidth,
                    curr_y + charHeight * k + charHeight * 3 / 4) + 1;

                console.log("delta");
                console.log(frame[k]);
                console.log(heap[frame[k][1][1]][0]);

                if (valid) {
                    if (is_box) {
                        console.log(depth);
                        h += depth * (minWidth + 15);
                    } else {
                        h += charHeight;
                    }
                }
                console.log(h);
            }
        }
        container.text(frame[0][0]).font("family", "Monaco, monospace").font("size", 14).dx(25).dy(curr_y);
        let rect = container.rect(maxlen * charWidth + 10, charHeight * frame.length + 10)
            .dx(15).dy(curr_y)
            .stroke({color: "#000000", width: 2})
            .fill({color: "#FFFFFF"})
            .radius(10).back();

        if (frame !== active_frame_data) {
            rect.attr("stroke-dasharray", "4");
        }

        curr_y += charHeight * frame.length + 20;
    }
}

let minWidth = charWidth * 4 + 5;

function calc_content_length(elem) {
    if (elem[0]) {
        return minWidth;
    } else {
        return Math.max(minWidth, charWidth * elem[1].length + 10);
    }
}

function straight_arrow(container, x1, y1, x2, y2) {
    container.circle(5).dx(x1 - 5 / 2).dy(y1 - 5 / 2);
    let arrow = container
        .polygon('0,0 -10,5 -10,-5')
        .dx(x2).dy(y2)
        .rotate(180 / Math.PI * Math.atan2(y2 - y1, x2 - x1), x2, y2);
    let length = Math.hypot(x2 - x1, y2 - y1);
    container
        .line(x1, y1, x2 + (x1 - x2) / length * 5, y2 + (y1 - y2) / length * 5)
        .stroke({width: 2, color: "#000000"});
}

function curved_arrow(container, x1, y1, x2, y2) {
    straight_arrow(container, x1, y1, x2, y2);
}

function display_elem(x, y, id, all_data, container, depth, cache, index, x1 = false, y1 = false) {
    if (id[0]) {
        // non atomic
        let data = all_data[id[1]];

        if (data[0] === "promise") {
            // console.log(index);
            // console.log(data[1][0]);
            if (index >= data[1][0]) {
                data = [data[1][1]];
            } else {
                data = [[false, "···"]];
            }
        }
        if (!x1) {
            x1 = x + minWidth / 2;
            y1 = y + minWidth / 2;
        }
        if (cache.has(id[1])) {
            curved_arrow(container, x1, y1, ...cache.get(id[1]));
            return 0;
        }
        let x2, y2;
        if (depth === 0) {
            cache.set(id[1], [x, y]);
            x2 = x + minWidth + 15;
            y2 = y + minWidth / 2;
            x = x2;
        } else {
            x2 = x + minWidth / 2;
            y2 = y + (minWidth + 15) * depth;
            y = y2;
        }
        if (data.length > 1) {
            straight_arrow(container, x1, y1, x2, y2);
        } else {
            straight_arrow(container, x1, y1, x, y + minWidth / 2);
        }
        cache.set(id[1], [x, y + minWidth / 2]);

        let pos = 0;
        let lens = [];
        for (let elem of data) {
            lens.push(pos);
            pos += calc_content_length(elem);
        }

        let new_depth = 0;
        for (let i = data.length - 1; i >= 0; --i) {
            if (i !== 0) {
                container.line(x + lens[i], y, x + lens[i], y + minWidth).stroke({color: "#000000", width: 2});
            }
            let elem = data[i];
            if (i !== data.length - 1 && elem[0] && !cache.has(elem[1])) {
                new_depth += 1;
            }
            new_depth += display_elem(x + lens[i], y, elem, all_data, container, new_depth, cache, index);
        }

        if (all_data[id[1]][0] === "promise") {
            container.circle(minWidth)
                .dx(x).dy(y)
                .stroke({color: "#000000", width: 2})
                .fill({color: "#FFFFFF"}).back();
        } else if (data.length > 1) {
            container.rect(pos, minWidth)
                .dx(x).dy(y)
                .stroke({color: "#000000", width: 2})
                .fill({color: "#FFFFFF"}).back();
        }
        // container.text(new_depth.toString(10)).dx(x).dy(y);
        return new_depth;
    } else {
        // atomic
        let width = calc_content_length(id);
        container.text(id[1])
            .font("family", "Monaco, monospace").font("size", 14)
            .cx(x + width / 2)
            .cy(y + minWidth / 2);
        // container.text("0").dx(x).dy(y);
        return 0;
    }
}
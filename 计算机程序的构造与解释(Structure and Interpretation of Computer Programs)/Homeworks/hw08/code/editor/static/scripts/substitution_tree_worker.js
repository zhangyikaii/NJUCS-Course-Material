import {
    states
} from "./state_handler";
import {
    charWidth
} from "./measure";
import {
    charHeight
} from "./measure";
import {get_active_node} from "./navigation";

import {javastyle} from "./settings";

export {
    display_tree,
    get_i
};

function display_str(elem) {
    if (elem["transition_type"] === "EVALUATED") {
        return elem["str"];
    }

    let children;
    if (elem["transition_type"] === "APPLYING") {
        children = elem["prev_children"];
    } else {
        children = elem["children"]
    }

    if (children.length === 0) {
        return elem["str"];
    }

    let out = "(";
    for (let child of children) {
        out += display_str(child) + " ";
    }
    out = out.slice(0, -1) + ")";
    return out;
}

async function locate(data) {
    await $.post("./reformat",
        {
            code: [display_str(data)],
            javastyle: javastyle()
        }).done(
        (response) => {
            response = $.parseJSON(response);
            data["str"] = response["formatted"];
        }
    );
    await _locate(data, data["str"], 0, 0, 0);
    data["root"] = true;
}

async function _locate(elem, base_str, i, row, col) {
    let pos = 0;
    let start_row = -1;
    let start_col = -1;
    let start_i = -1;

    let max_col = -1;

    elem["root"] = false;

    let display_elem_str = display_str(elem);

    while (base_str[i] === " " || base_str[i] === "\n" || base_str[i] === display_elem_str[pos]) {
        if (base_str[i] === display_elem_str[pos] && start_row === -1) {
            start_row = row;
            start_col = col;
            max_col = col;
            start_i = i;
        }
        if (base_str[i] === display_elem_str[pos]) {
            ++pos;
        }
        if (pos === display_elem_str.length) {
            break;
        }
        if (base_str[i] === "\n") {
            ++row;
            col = 0;
        } else {
            ++col;
            max_col = Math.max(max_col, col);
        }
        ++i;
    }

    if (pos !== display_elem_str.length) {
        console.error("Misaligned debug output!");
    }

    elem["start_row"] = start_row;
    elem["start_col"] = start_col;
    elem["start_i"] = start_i;
    elem["end_row"] = row;
    elem["end_col"] = max_col;
    elem["end_i"] = i;

    let child_i = start_i + 1;
    let child_row = start_row;
    let child_col = start_col + 1;

    for (let child of elem["children"]) {
        if (elem["transition_type"] === "APPLYING") {
            await locate(child);
        } else {
            await _locate(child, base_str, child_i, child_row, child_col);
            child_i = child["end_i"] + 1;
            child_row = child["end_row"];
            child_col = child["end_col"] + 1;
        }
    }
}

function get_i(all_data, curr, i) {
    let labels = [
        ["transitions", "transition_type"],
        ["strs", "str"],
        ["parent_strs", "parent_str"],
    ];
    let data = {};
    let transition_time = {};
    for (let label of labels) {
        for (let val of all_data[curr][label[0]]) {
            if (val[0] > i) {
                break;
            }
            transition_time[label[1]] = val[0];
            data[label[1]] = val[1];
        }
    }

    let j;

    for (j = 0; j < all_data[curr]["children"].length - 1; ++j) {
        if (all_data[curr]["children"][j + 1][0] > i) {
            break;
        }
    }

    data["id"] = curr;

    data["children"] = [];
    for (let child of all_data[curr]["children"][j][1]) {
        data["children"].push(get_i(all_data, child, i));
    }

    data["prev_children"] = [];
    if (data["transition_type"] === "APPLYING") {
        for (j = 0; true; ++j) {
            if (all_data[curr]["children"][j][0] >= transition_time["transition_type"]) {
                break;
            }
        }
        for (let child of all_data[curr]["children"][j - 1][1]) {
            data["prev_children"].push(get_i(all_data, child, i));
        }
    }

    return data;
}

async function display_tree(id, svg, clear_svg, is_tree) {
    let data = get_i(
        states[id].states[states[id].expr_i][2],
        states[id].roots[states[id].expr_i],
        states[id].index,
    );

    if (!is_tree) {
        await locate(data);
    }

    let active_node = get_active_node(id, true);

    clear_svg();
    svg.clear();

    if (is_tree) {
        _display_tree(data, svg, 10, 15 + !states[id].up_to_date * 25, 0, [0]);
    } else {
        _display_debug(data, svg, active_node, 10 + !states[id].up_to_date * 25);
    }
}

function _display_tree(data, container, x, y, level, starts) {
    let color;
    switch (data["transition_type"]) {
        case "UNEVALUATED":
            color = "#536dff";
            break;
        case "EVALUATING":
            color = "#ff0f00";
            break;
        case "EVALUATED":
            color = "#44ff51";
            break;
        case "APPLYING":
            color = "#ffa500";
            break;
    }

    container.rect(data["str"].length * charWidth + 10, charHeight + 10)
        .dx(x - 5).dy(y)
        .stroke({color: color, width: 2})
        .fill({color: "#FFFFFF"})
        .radius(10);

    container.text(data["str"]).font("family", "Monaco, monospace").font("size", 14).dx(x).dy(y);
    let xDelta = charWidth;

    starts[level] = x + charWidth * (data["str"].length + 1);
    for (let child of data["children"]) {
        if (starts.length === level + 1) {
            starts.push([10]);
        }
        let parent_len = child["parent_str"].length * charWidth;
        container.line(x + xDelta + parent_len / 2, y + charHeight + 5,
            Math.max(x + xDelta - 100000, starts[level + 1]) + child["str"].length * charWidth / 2 + 5,
            y + 60)
            .stroke({width: 3, color: "#c8c8c8"}).back();
        _display_tree(child, container, Math.max(x + xDelta - 100000, starts[level + 1]), y + 50, level + 1, starts);
        xDelta += parent_len + charWidth;
    }
}


function _display_debug(data, container, active_id, base_y, base_h) {
    if (base_h === undefined) {
        base_h = data["str"].split("\n").length * charHeight;
    }
    let color;
    switch (data["transition_type"]) {
        case "UNEVALUATED":
            color = "transparent";
            break;
        case "EVALUATING":
            color = "#ff0f00";
            break;
        case "EVALUATED":
            color = "#44ff51";
            break;
        case "APPLYING":
            color = "#ffa500";
            break;
    }

    let width = charWidth * (data["end_col"] - data["start_col"] + 1);
    let height = charHeight * (data["end_row"] - data["start_row"] + 1);

    let x = data["start_col"] * charWidth + 10;
    let y = data["start_row"] * charHeight + base_y;

    let rect = container.rect(width + 5, height + 5).dx(x - 3).dy(y)
        .stroke({
            color: color,
            width: 2
        })
        .radius(5)
        .fill("transparent");

    let is_important = data["id"] === active_id || data["transition_type"] === "APPLYING";

    if (!is_important) {
        rect.attr("stroke-dasharray", "1 3");
    }

    if (data["root"]) {
        rect.fill({
            color: "#FFFFFF"
        });
        let lines = data["str"].split("\n");
        for (let line = 0; line !== lines.length; ++line) {
            container.text(lines[line]).font("family", "Monaco, monospace").font("size", 14).dx(x).dy(y + charHeight * line)
                .attr('xml:space', 'preserve', 'http://www.w3.org/XML/1998/namespace');
        }
    }

    let xDelta = charWidth;

    for (let child of data["children"]) {
        let parent_len = child["parent_str"].length * charWidth;
        if (data["transition_type"] === "APPLYING") {
            _display_debug(child, container, active_id, base_y + base_h + 10);
        } else {
            _display_debug(child, container, active_id, base_y, base_h);
        }
        xDelta += parent_len + charWidth;
    }

    if (is_important && !data["root"]) {
        rect.front();
    }
}
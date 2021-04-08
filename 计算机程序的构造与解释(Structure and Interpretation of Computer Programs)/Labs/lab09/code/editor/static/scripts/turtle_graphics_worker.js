export {draw};

function draw(svg, rawSVG, data) {
    $(rawSVG).css("background-color", data["bgColor"]);
    for (let move of data["path"]) {
        svg.path(move["seq"])
            .fill(move["fill"])
            .stroke({color: move["stroke"], width: 1, linecap: 'round', linejoin: 'round'});
    }

    if (data["showTurtle"]) {
        svg.polygon('0,0 -10,5 -10,-5')
            .dx(data["turtleX"]).dy(data["turtleY"])
            .rotate(data["turtleRot"], data["turtleX"], data["turtleY"]);
    }
}
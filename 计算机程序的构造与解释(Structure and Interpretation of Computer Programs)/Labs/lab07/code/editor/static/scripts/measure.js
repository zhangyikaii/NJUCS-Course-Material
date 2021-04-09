export { charHeight, charWidth };

function getDims(parentElement) {
    parentElement = parentElement || document.body;
    let div = document.createElement('div');
    $(div).css("position", "absolute");
    $(div).css("white-space", "pre-line");
    $(div).css("font-family", "Monaco, monospace");
    $(div).css("font-size", "14px");

    div.innerHTML = "x".repeat(999) + "x\n".repeat(1000);
    parentElement.appendChild(div);
    let w = div.offsetWidth / 1000;
    let h = div.offsetHeight / 1001;
    parentElement.removeChild(div);
    return [w, h];
}

let charHeight = getDims()[1];
let charWidth = getDims()[0];
export {init}

function init() {
    $("#documentation-search").on("input", function () {
        let text = $("#documentation-search").val();
        $("#documentation-search").val("");
        $("#documentation-search-modal").val(text);
        $("#documentationModal").modal("show");
        $("#documentation-search-modal").focus();
        render($("#documentation-search-modal").val());
    });

    $("#documentation-search-modal").on("input", function () {
        render($("#documentation-search-modal").val());
    });

    $('.documentation-form').on('keyup keypress', function(e) {
      let keyCode = e.keyCode || e.which;
      if (keyCode === 13) {
        e.preventDefault();
        return false;
      }
    });
}

function render(query) {
    $.post("./documentation", {
        query: query,
    }).done(function (data) {
        data = $.parseJSON(data);
        console.log(data);
        $("#documentation-body").empty();
        for (let elem of data) {
            $("#documentation-body").append(
                "<li class=\"list-group-item\">" + elem + "</li>");
        }
    });
}
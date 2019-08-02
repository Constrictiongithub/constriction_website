require("bootstrap/js/dist/button");
$(function () {
    $("#enable-all-countries").on("click", function(event){
        event.preventDefault();
        $(".filters input[name='country']:not(:checked)").trigger("click");
    });

    $("#disable-all-countries").on("click", function (event) {
        event.preventDefault();
        $(".filters input[name='country']:checked").trigger("click");
    });
});
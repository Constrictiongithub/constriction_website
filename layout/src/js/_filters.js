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

    $("#enable-all-categories").on("click", function(event){
        event.preventDefault();
        $(".filters input[name='category']:not(:checked)").trigger("click");
    });

    $("#disable-all-categories").on("click", function (event) {
        event.preventDefault();
        $(".filters input[name='category']:checked").trigger("click");
    });

    $(".thousandseparator").on("textInput input", function(){
        var ts = $(this).data("thousandseparator"),
            val = $(this).val().split(ts).join(""),
            splitted = val.split( /(?=(?:...)*$)/ );
        if(splitted) res = splitted.shift();
        splitted.forEach(function(split){
            res += ts + split
        });
        $(this).val(res);
    });
    $("form").on("submit", function(){
        $(this).find(".thousandseparator").each(function(){
            var ts = $(this).data("thousandseparator");
            $(this).val($(this).val().split(ts).join(""));
        });
    });
});
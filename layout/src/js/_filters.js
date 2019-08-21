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

    $(".thousandseparator").on("keyup", function(event){
        var ts = $(this).data("thousandseparator"),
            val = $(this).val().split(ts).join(""),
            splitted = val.split( /(?=(?:...)*$)/ );
        if(splitted) res = splitted.shift();
        splitted.forEach(function(split){
            res += ts + split
        });
        $(this).val(res);
    }).trigger("keyup");

    $(".percentage").on("keyup", function(event){
        var keyCode = event.keyCode,
            val = $(this).val().split("%").join("");
        if (keyCode == 8) val = val.substring(0, val.length - 1);
        if (val) val += "%";
        $(this).val(val);
    }).trigger("keyup");

    $("form").on("submit", function(){
        $(this).closest("form").find(".thousandseparator").each(function(){
            var ts = $(this).data("thousandseparator");
            $(this).val($(this).val().split(ts).join(""));
        });
        $(this).closest("form").find(".percentage").each(function(){
            $(this).val($(this).val().split("%").join(""));
        });
    });
});
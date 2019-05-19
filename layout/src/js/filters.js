require("bootstrap/js/dist/button");

$(function () {
    function refreshInputs($element){
        const $button = $(".dropdown-button[data-target='#" + $element.attr("id") + "']");
        if ($element.hasClass("filter-checkbox") ){
            if ($element.find("input[type='checkbox']:not(:checked)").length) {
                $button.addClass("checked");
            }
            else{
                $button.removeClass("checked");
            }
        }
        if ($element.hasClass("filter-text")) {
            if ($element.data("default") === $element.find("input").val()){
                $button.removeClass("checked");
            }
            else {
                $button.addClass("checked");
            }
        }
    }
    
    /*$(".dropdown-content").on("change", "input", function(evt){
        refreshInputs($(evt.delegateTarget));
    });*/

    $(".dropdown-content").each(function(){
        refreshInputs($(this));
    });
});
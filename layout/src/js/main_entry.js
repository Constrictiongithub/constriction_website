import "../scss/main.scss";
require("./font-awesome.js");
require("bootstrap/js/dist/collapse");
require("./filters.js");

$(function () {
    var navMain = $(".navbar-collapse");
    navMain.on("click", "a:not([data-toggle])", null, function () {
        navMain.collapse('hide');
    });
});
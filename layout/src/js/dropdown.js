$(function () {
    function closeDropdown($button) {
        $($button.data("target")).slideUp("fast").attr("aria-hidden", "true");
        $button.attr("aria-expanded", "false");
    }

    function openDropdown($button) {
        $button.closest(".dropdown-group").find(".dropdown-button").each(function () {
            closeDropdown($(this));
        });
        $($button.data("target")).slideDown("fast").attr("aria-hidden", "false");
        $button.attr("aria-expanded", "true");
    }

    $(".dropdown-button").on("click", function (evt) {
        if ($(this).attr("aria-expanded") === "true") {
            closeDropdown($(this));
        } else {
            openDropdown($(this));
        }
    });
});
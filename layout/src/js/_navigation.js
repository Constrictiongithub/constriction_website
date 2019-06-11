$(function () {
    // SMOOTH SCROLLING
    function scrollToPosition(event) {
        // On-page links
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            // Figure out element to scroll to
            var $target = $(this.hash);
            if ($target.length && $target.data("toggle")) {
                // Only prevent default if animation is actually gonna happen
                if (event){
                    event.preventDefault();
                }
                var $navbar_fixed = $("body .navbar.fixed-top");
                var navbarOffset = $navbar_fixed.length && $navbar_fixed.height() || 0;
                $('html, body').animate({
                    scrollTop: ($target.offset().top - navbarOffset)
                }, 1000, function () {
                    // Callback after animation
                    var hash = "#" + $target.attr("id");
                    if (history.pushState) {
                        history.pushState(null, null, hash);
                    } else {
                        location.hash = hash;
                    }
                    $('#main-menu a[href*="#"]').removeClass("active");
                    if (location.hash) {
                        $('#main-menu a[href*="' + location.hash + '"]').addClass("active");
                    } else {
                        $('#main-menu a[href*="#hp"]').addClass("active");
                    }
                });
            }
        }
    }
    $('a[href*="#"]').on("click", scrollToPosition);
    if (location.hash){
        $('a[href *= "' + location.hash + '"]').trigger("click");
    }
});
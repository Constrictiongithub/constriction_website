require("bootstrap/js/dist/collapse");

$(function () {
    // CLOSES THE COLLAPSIBLE
    var navMain = $(".navbar-collapse");
    navMain.on("click", "a:not([data-toggle])", null, function () {
        navMain.collapse('hide');
    });
    // Set active element on load based on hash
    function setActiveMenuItem(){
        $('#main-menu a[href*="#"]').removeClass("active");
        if (window.location.hash) {
            $('#main-menu a[href*="' + window.location.hash + '"]').addClass("active");
        } else {
            $('#main-menu a[href*="#hp"]').addClass("active");
        }
    }
    setActiveMenuItem();

    // SMOOTH SCROLLING
    $('a[href*="#"]').click(function (event) {
        // On-page links
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            // Figure out element to scroll to
            var $target = $(this.hash);
            if ($target.length) {
                // Only prevent default if animation is actually gonna happen
                event.preventDefault();
                var $navbar_fixed = $("body .navbar.fixed-top");
                var navbarOffset = $navbar_fixed.length && $navbar_fixed.height() || 0;
                $('html, body').animate({
                    scrollTop: ($target.offset().top - navbarOffset)
                }, 1000, function () {
                    // Callback after animation
                    // Must change focus!
                    var hash = "#" + $target.attr("id");
                    if (history.pushState) {
                        history.pushState(null, null, hash);
                    } else {
                        location.hash = hash;
                    }
                    setActiveMenuItem();
                });
            }
        }
    });
});
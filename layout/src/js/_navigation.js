$(function () {

    var $navbar_fixed = $("body .navbar.fixed-top");
    var navbarOffset = $navbar_fixed.length && $navbar_fixed.height() || 0;

    // SMOOTH SCROLLING
    function scrollToPosition(event) {
        // On-page links
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            // Figure out element to scroll to
            var $target = $(this.hash);
            if ($target.length && !$target.data("toggle")) {
                // Only prevent default if animation is actually gonna happen
                if (event){
                    event.preventDefault();
                }
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
                });
            }
        }
    }
    $('a[href*="#"]').on("click", scrollToPosition);
    if (location.hash){
        $('a[href *= "' + location.hash + '"]').trigger("click");
    }
    $(window).scroll(function () {
        var scrollPos = $(window).scrollTop();
        $('.anchor').each(function (index, element) {
            var topPos = $(element).offset().top;
            if ((topPos - scrollPos) <= navbarOffset) {
                $('#main-menu .nav-link.active').removeClass('active');
                $('#main-menu a[href*="' + $(element).attr("id") + '"]').addClass("active");
            }
        })
    });
    $(window).scroll();
});
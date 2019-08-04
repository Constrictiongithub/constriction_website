$(function () {

    var $navbar_fixed = $("body .navbar.fixed-top");
    var navbarOffset = $navbar_fixed.length && $navbar_fixed.height() || 0;

    // SMOOTH SCROLLING
    function scrollToPosition($target){
        $('html, body').animate({
            scrollTop: ($target.offset().top - navbarOffset)
        }, 750, function () {
            // Callback after animation
            var hash = "#" + $target.attr("id");
            if (history.pushState) {
                history.pushState(null, null, hash);
            } else {
                location.hash = hash;
            }
        });
    }

    function scrollToLink(event) {
        // On-page links
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            // Figure out element to scroll to
            var $target = $(this.hash);
            if ($target.length && !$target.data("toggle")) {
                // Only prevent default if animation is actually gonna happen
                event.preventDefault();
                scrollToPosition($target);
            }
        }
    }

    // TODO:  throttle to run at max every 100ms
    $(window).scroll(function () {
        if ($(".hp").length > 0){
            var scrollPos = $(window).scrollTop();
            $('.anchor').each(function (index, element) {
                var topPos = $(element).offset().top;
                if ((topPos - scrollPos) < navbarOffset + 10) {
                    $('#main-menu .nav-item.active').removeClass('active');
                    $('#main-menu a.nav-link[href*="' + $(element).attr("id") + '"]').closest(".nav-item").addClass("active");
                }
                if (scrollPos + $(window).height() == $(document).height()){
                    $('#main-menu .nav-item.active').removeClass('active');
                    $('#main-menu a.nav-link').last().closest(".nav-item").addClass("active");
                }
            });
        }
    });
    
    $(window).scroll();

    $('a[href*="#"]').on("click", scrollToLink);

    if (location.hash && $(location.hash).length > 0){
        scrollToPosition($(location.hash));
    }

});
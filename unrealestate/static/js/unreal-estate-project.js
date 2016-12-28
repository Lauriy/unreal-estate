(function ($) {
    'use strict';
    /*jslint nomen: true*/
    /*jslint browser: true*/
    $(document).ready(function () {
        var $sliders = $('.slider');
        if ($sliders.length > 0) {
            $sliders.slidertron({
                mode: 'fadeIn',
                seamlessWrap: true,
                viewerSelector: '.viewer',
                reelSelector: '.viewer .reel',
                slidesSelector: '.viewer .reel .slide',
                advanceDelay: 0,
                speed: 400,
                fadeInSpeed: 1000,
                autoFit: true,
                autoFitAspectRatio: (840 / 344),
                navPreviousSelector: '.nav-previous',
                navNextSelector: '.nav-next',
                indicatorSelector: '.indicator ul li',
                slideLinkSelector: '.link'
            });
            $(window).on('resize load', function () {
                $sliders.trigger('slidertron_reFit');
            }).trigger('resize');
        }
    });
}(jQuery));
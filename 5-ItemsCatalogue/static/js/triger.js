$(document).ready(function () {
    "use strict";


    $(".social-slider").owlCarousel({
        stagePadding: 0,
        margin: 0,
        Number: 10,
        rewindNav: false,
        pagination: false,
        autoplay: true, //Set AutoPlay to 3 seconds
        autoplaySpeed: 1000,
        stopOnHover: true,
        responsiveClass: true,
        dots: false,
        loop: true,
        responsive: {
            0: {
                items: 1,
            },
            700: {
                items: 3,
            },
            960: {
                items: 4,

            },
            1024: {
                items: 4,

            },
            1025: {
                items: 5,

            },
            1281: {
                items: 6,

            }
        }

    });
    $(".testimonial").owlCarousel({
        stagePadding: 0,
        margin: 30,
        rewindNav: false,
        pagination: false,
        autoplay: false, //Set AutoPlay to 3 seconds
        autoplaySpeed: 1000,
        stopOnHover: true,
        responsiveClass: true,
        dots: false,
        loop: true,
        responsive: {
            0: {
                items: 1,
            },
            700: {
                items: 1,
            },
            960: {
                items: 2,

            },
            1024: {
                items: 2,

            },
            1025: {
                items: 2,

            },
            1281: {
                items: 2,

            }
        }

    });
    $(".cat-slider").owlCarousel({
        stagePadding: 0,
        margin: 30,
        rewindNav: false,
        pagination: true,
        autoplay: false, //Set AutoPlay to 3 seconds
        autoplaySpeed: 1000,
        stopOnHover: true,
        responsiveClass: true,
        dots: false,
        loop: true,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 1,
            },
            700: {
                items: 2,
            },
            960: {
                items: 3,

            },
            1024: {
                items: 3,

            },
            1025: {
                items: 4,

            },
            1281: {
                items: 4,

            }
        }

    });

    setInterval(function () {
        $('.feature-slider').each(function () {

            var $mycarousel = $(this);

            $mycarousel.owlCarousel({

                autoplay: $mycarousel.data("autoplay"),
                autoplaySpeed: 100,
                items: $mycarousel.data("items"),
                margin: $mycarousel.data("gutter"),
                loop: $mycarousel.data("loop"),
                navigation: true,
                merge: true,
                autoplayHoverPause: true,
                responsiveRefreshRate: 1,
                nav: $mycarousel.data("nav"),
                navText: ["<i class='helpme-icon-angle-left'></i>", "<i class='helpme-icon-angle-right'></i>"],
                autoplayTimeout: $mycarousel.data("autoplay-delay"),
                responsive: {
                    0: {
                        items: 1,
                    },
                    700: {
                        items: $mycarousel.data("items-tab"),
                    },
                    960: {
                        items: $mycarousel.data("items-tab-ls"),

                    },
                    1025: {
                        items: $mycarousel.data("items"),

                    }
                }
            });
        });
    }, 100);

});
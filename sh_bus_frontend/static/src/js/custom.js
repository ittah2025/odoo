// Counter Variables Individual per snippet
var s_5 = 0;

/*
 * Windows scroll start here
 */
$(window).scroll(function () {
    /*
     * ******************************************************************************
     * counter 1 start here
     * *****************************************************************************
     */
    // if check element exist
    if ($("#sh_counter_section").length) {
        var oTop = $("#sh_counter_section").offset().top - window.innerHeight;
        if (s_5 == 0 && $(window).scrollTop() > oTop) {
            //counter part start here
            $("#sh_counter_section .sh_count_name")
                .each(function () {
                    var $this = $(this);
                    looping = true;
                    jQuery({ Counter: 0 }).animate(
                        { Counter: $this.text() },
                        {
                            duration: 8000,
                            easing: "swing",
                            step: function () {
                                $this.text(Math.ceil(this.Counter));
                            },
                        }
                    );
                })
                .promise()
                .done(function () {
                    looping = false;
                });
            //counter part ends here

            s_5 = 1;
        }
    }
});

// OWL SLIDER //

/*$(document).ready(function () {
    $("#sh_testimonial .owl-carousel").owlCarousel({
        items: 2,
        loop: true,
        margin: 10,
        autoplay: true,
        dots: true,
        autoplaySpeed: 1000,
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 1,
            },
            1000: {
                items: 2,
            },
        },
    });
});*/

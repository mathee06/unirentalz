// -------------------------------------------------------------------------------------------
// empty links return false

$(document).ready(function(){
    $('a[href=#]').click(function (event) {
        event.preventDefault();
    });
    // fix html5 placeholder attribute for ie7 & ie8
    if ($.browser.msie && $.browser.version.substr(0, 1) < 9) { // ie7&ie8
        $('input[placeholder], textarea[placeholder]').each(function () {
            var input = $(this);

            $(input).val(input.attr('placeholder'));

            $(input).focus(function () {
                if (input.val() == input.attr('placeholder')) {
                    input.val('');
                }
            });

            $(input).blur(function () {
                if (input.val() == '' || input.val() == input.attr('placeholder')) {
                    input.val(input.attr('placeholder'));
                }
            });
        });
    }
});

// -------------------------------------------------------------------------------------------
// init default skin
$(document).ready(function() {
    if(!$(".style-switcher").length) {
        var skin = 'light'; // light or dark

        $('#css-switcher-link').attr('href', 'assets/css/theme-' + skin + '.css');
        $('#partners img, div.logo img').each(function () {
            arr = $(this).attr('src').split('/');
            $(this).attr('src', 'assets/img/' + skin + '/' + arr[arr.length - 1]);
        });
    }
});

// -------------------------------------------------------------------------------------------
// superfish menu

$(document).ready(function() {
    $('ul.sf-menu').superfish();
    // -------------------------------------------------------------------------------------------
    // create mobile menu from exist superfish menu

    $(document).ready(function () {
        var $menu = $('.site-navigation > ul'),
            optionsList = '<option value="" selected> - - Main Navigation - - </option>';

        $menu.find('li').each(function () {
            var $this = $(this),
                $anchor = $this.children('a'),
                depth = $this.parents('ul').length - 1,
                indent = '';

            if (depth) {
                while (depth > 0) {
                    indent += ' ::: ';
                    depth--;
                }
            }

            optionsList += '<option value="' + $anchor.attr('href') + '">' + indent + ' ' + $anchor.text() + '</option>';
        }).end().parent().parent().find('#res-menu').append('<select class="res-menu">' + optionsList + '</select><div class="res-menu-title">Navigation <i class="fa fa-angle-down"></i></div>');

        $('.res-menu').on('change', function () {
            window.location = $(this).val();
        });

    });
});

// prettyPhoto
$(document).ready(function(){
    $("a[data-gal^='prettyPhoto']").prettyPhoto({theme:'dark_square'});
});

// sign in/up form
$(document).ready(function(){
    $('.signin-link, .signin-form button').click(function(){
        $('.signin-form').fadeToggle();
        if($('.signup-form').is(":visible")) {
            $('.signup-form').fadeToggle();
        }
    });
    $('.signup-link, .signup-form button').click(function(){
        $('.signup-form').fadeToggle();
        if($('.signin-form').is(":visible")) {
            $('.signin-form').fadeToggle();
        }
    });
});

// make google map search draggable
$(document).ready(function(){
    if($(".gmap-search").length){
        $(".gmap-search").draggable();
    }
});

// -------------------------------------------------------------------------------------------
// Rent/Buy switcher

$(document).ready(function(){
    $('.rent-buy a').click(function(){
        $('.rent-buy a').removeClass('active');
        $(this).addClass('active');
    });
});

// -------------------------------------------------------------------------------------------
// add hover class

var hover = $('.thumbnail');
hover.hover(
    function () {
        $(this).addClass('hover')
    },
    function () {
        $(this).removeClass('hover')
    }
)

// -------------------------------------------------------------------------------------------
// Selectbox

$(window).on('load', function () {
    $('.selectpicker').selectpicker();
});

// -------------------------------------------------------------------------------------------
// Isotope

$(window).resize(function () {
    // relayout on window resize
    $('.projects .items').isotope('reLayout');
});

$(window).load(function () {
    // cache container
    var $container = $('.projects .items');
    // initialize isotope
    $container.isotope({
        // options...
        itemSelector: '.item'
    });
    // filter items when filter link is clicked
    $('#filtrable a').click(function () {
        var selector = $(this).attr('data-filter');
        $("#filtrable li").removeClass("current");
        $(this).parent().addClass("current");
        $container.isotope({ filter: selector });
        return false;
    });
    $container.isotope('reLayout');
});

$(window).resize(function () {
    // relayout on window resize
    $('.gallery .items').isotope('reLayout');
});

$(window).load(function () {
    // cache container
    var $container = $('.gallery .items');
    // initialize isotope
    $container.isotope({
        // options...
        itemSelector: '.item'
    });
    // filter items when filter link is clicked
    $('#filtrable a').click(function () {
        var selector = $(this).attr('data-filter');
        $("#filtrable li").removeClass("current");
        $(this).parent().addClass("current");
        $container.isotope({ filter: selector });
        return false;
    });
});


// -------------------------------------------------------------------------------------------
// royalSlider

$(window).load(function() {
    if ($.fn.royalSlider) {
        $(".royalSlider").royalSlider({
            fullscreen: {
                enabled: false,
                nativeFS: true
            },
            imageScalePadding: 0,
            controlNavigation: 'thumbnails',
            thumbs: {
                orientation: 'vertical',
                spacing: 10,
                paddingBottom: 0,
                appendSpan: true,
                arrowLeft:$('.rsThumbsArrowLeft'),
                arrowRight:$('.rsThumbsArrowRight'),
                fitInViewport:false
            },
            transitionType:'fade',
            autoScaleSlider: false,
            loop: true,
            arrowsNav: false,
            keyboardNavEnabled: true
        });
    }
});

// -------------------------------------------------------------------------------------------
// Owl Carousel

$(document).ready(function () {
    $("#featured").owlCarousel({
        items: 3,
        itemsDesktop: false,
        itemsDesktopSmall: [991, 2],
        itemsTablet: false,
        itemsMobile: [479, 1],
        autoPlay: true,
        pagination: false
    });
    $(".featured-next").click(function () {
        $("#featured").trigger('owl.next');
        return false;
    });
    $(".featured-prev").click(function () {
        $("#featured").trigger('owl.prev');
        return false;
    });
    $("#testimonials").owlCarousel({
        items: 2,
        itemsDesktop: false,
        itemsDesktopSmall: [991, 2],
        itemsTablet: [768, 1],
        itemsMobile: [479, 1],
        autoPlay: true,
        pagination: false
    });
    $("#partners").owlCarousel({
        items: 6,
        itemsDesktop: false,
        itemsDesktopSmall: [991, 5],
        itemsTablet: [768, 3],
        itemsMobile: [479, 2],
        autoPlay: true,
        pagination: false
    });
    $("#last-tweets").owlCarousel({singleItem: true, autoPlay: true, pagination: false });

});

// -------------------------------------------------------------------------------------------
// Animation

var i = 0;
var anim_offset = 50;
var w_height = $(window).height();

function do_block_animation() {

    var sections = $('.animate-me');

    $(window).scroll(function () {
        sections.each(function () {
            var section = $(this);
            if (!section.hasClass('animate-off') && (w_height + $(window).scrollTop() - section.offset().top - anim_offset > 0)) {
                section.addClass('animate-off').trigger('start_animation');
                i++;
            }
        });
    });

    sections.bind('start_animation', function () {
        var section = $(this);
        if (i & 1) {
            section.addClass('animated bounceInRight');
        }
        else {
            section.addClass('animated bounceInLeft');
        }
        //section.one('webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd', $(this).css({'opacity': 1}));
    });

    $(window).resize(function () {
        w_height = $(window).height();
    });
}

function is_block_visible() {

    var sections = $('' +
        // blog
        '.btn, socical-line a' +
        '.full-width > .container div' +
        //'.row' +
        //'.row > div' +
        //', body > .container' +
        //', body > .container > div' +
        //', body > .full-width > .container > div' +
        //
        '');
    //var sections = $('div.row > div');

    sections.each(function () {
        var section = $(this);
        if (!section.hasClass('animate-off') && (w_height + $(window).scrollTop() - section.offset().top - anim_offset > 0)) {
            section.addClass('animate-off');
        } else {
            //section.css({'opacity': 0});
            section.addClass('animate-me');
        }
    });
}

$(document).ready(function () {
    is_block_visible();
    do_block_animation();
});


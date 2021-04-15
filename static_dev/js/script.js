$(document).ready(function () {
    var isMobile = false,
        isApple = false,
        wHeight = document.body.clientHeight;

    if (navigator.userAgent.match(/Android/i) ||
        navigator.userAgent.match(/webOS/i) ||
        navigator.userAgent.match(/iPhone/i) ||
        navigator.userAgent.match(/iPad/i) ||
        navigator.userAgent.match(/iPod/i) ||
        navigator.userAgent.match(/IEMobile/i) ||
        navigator.userAgent.match(/BlackBerry/i)) {
        isMobile = true;
    };

    if (navigator.userAgent.match(/iPhone/i) ||
        navigator.userAgent.match(/iPad/i) ||
        navigator.userAgent.match(/iPod/i)) {
        isApple = true;
    };


    const observer = lozad('.lozad');
    observer.observe();


    // up! button
    $(function () {
        $('<img id="go-top" src="/static/img/icons/white-down.svg">').appendTo('body');
        $('#go-top').css({
            'opacity': '0',
            'visibility': 'hidden'
        });
        $(window).scroll(function () {
            if ($(this).scrollTop() > 500) {
                $('#go-top').css({
                    'opacity': '1',
                    'visibility': 'visible'
                });
            } else {
                $('#go-top').css({
                    'opacity': '0',
                    'visibility': 'hidden'
                });
            }
        });
        $('#go-top').click(function () {
            $('body,html').animate({
                scrollTop: 0
            }, 500);
            return false
        });
    });

    // fixed Header
    $(window).scroll(function () {

        if ($(window).scrollTop() >= 50) {
            $('header').addClass('fl-fix');
        }
        else {
            $('header').removeClass('fl-fix');
        }
    });

    // Prod qty
    $(document).on('click', '.product-item .plus,.add-name-price .plus,form.order-qty-mn .plus', function (e) {
        e.preventDefault();
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
    $(document).on('click', '.product-item .minus,.add-name-price .minus,form.order-qty-mn .minus', function (e) {
        e.preventDefault();
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });

    // Search filter


    const search = document.getElementById('searchproduct')

    search.addEventListener('keyup', function () {

        const word = this.value

        const url = window.location.origin + '/result/'

        fetch(`${url}?q=${word}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },

        }).then(res => res.json())
            .then(data => {

                document.querySelector('#search_list').innerHTML = ''
                $.each(data.products, function (k, v) {

                    $('#search_list').append(
                        '<li class="fast-search-item"><a href="' + v.slug + '">' +
                        '<img src="' + v.image + '">' + v.name + '</a>' +
                        '</li>'
                    );
                });
                $('#search-list-items').css('display', 'block');

                if (!this.value) {
                    $('#search-list-items').css('display', 'none');
                    return
                }

            }
            )

    })


    // languages
    $(document).click(function (event) {
        if ($(event.target).closest('.choose_lang', '.up-down-button').length) return;
        $('.choose_lang').slideUp('fast');
        $('.up-down-button').toggleClass('up-down-button');
        event.stopPropagation();
    });
    $('.choose').click(function () {
        $(this).siblings('.choose_lang').slideToggle('fast');
        $('.choose .down-icon').toggleClass('up-down-button');
        return false;
    });

    // search form
    $('#search-show').click(function () {
        $('.search-bar').fadeIn(10);
    });
    $('#search-close').click(function () {
        $('.search-bar').fadeOut(10);
    });

    //Cart
    $(function () {
        $(document).on("click", ".mobile_menu", function (e) {
            e.preventDefault();
            $('body').addClass('opened-noscroll');
            $(".cart_menu_container").addClass("loaded");
            $(".cart_menu_overlay").fadeIn("fast");
        });
        $(document).on("click", ".cart_menu_overlay,.close-side-widget", function (e) {
            $(".cart_menu_container").removeClass("loaded");
            $(this).fadeOut("fast");
            $('body').removeClass('opened-noscroll');
            $(".cart_menu_overlay").fadeOut("fast");
        });

        $(document).on("click", ".filter-bar", function (e) {
            e.preventDefault();
            $(".filter_menu_container").addClass("loaded");
            $(".filter_menu_overlay").fadeIn("fast");
        });
        $(document).on("click", ".filter_menu_overlay,.close-side-widget", function (e) {
            $(".filter_menu_container").removeClass("loaded");
            $(this).fadeOut("fast");
            $(".filter_menu_overlay").fadeOut("fast");
        });

    });

    //Menu
    $(function () {
        $(document).on("click", ".mobile_menu_container .parent", function (e) {
            e.preventDefault();
            $(this).siblings("ul").addClass("loaded");
        });
        $(document).on("click", ".mobile_menu_container .back", function (e) {
            e.preventDefault();
            $(this).parent().parent().removeClass("loaded");
        });
        $(document).on("click", ".menu-bar", function (e) {
            e.preventDefault();
            $(".mobile_menu_container").addClass("loaded");
            $(".mobile_menu_overlay").fadeIn("fast");
        });
        $(document).on("click", ".mobile_menu_overlay,.close-side-widget", function (e) {
            $(".mobile_menu_container").removeClass("loaded");
            $(this).fadeOut("fast");
            $(".mobile_menu_overlay").fadeOut("fast");
        });
    });

    $('#op-time').click(function () {
        $('.block-content').slideToggle('fast');
    });

    // Basket Message
    $(document).on('click', '.add-cart,.submit_btn', function (e) {
        $('#Messagebasket').removeClass('hidden').promise().done(function () {
            $('#Messagebasket').show().delay(2000).queue(function (n) {
                $(this).hide();
                n();
            });
        });

    });

    // cat icon
    $(function () {
        var $lenghtUl = $("li.sub-menu ul").find("li").length;
        if ($lenghtUl >= 1) {
            $('li.sub-menu').append('<img src="/static/img/icons/cat-down.svg" class="cat-left">');
            $('li.sub-menu > .cat-left').click(function () {
                $(this).parent().toggleClass('active');
                $(this).toggleClass('up-cat').parent().find('ul').first().slideToggle('fast');
            });
        }
    });

    // footer
    $(function () {
        $(".footer-item h4").click(function () {
            $(this).parent().toggleClass('active');
        });
    });

    $(function () {
        $(".filter-params-hint").click(function () {
            $(this).parent().parent().toggleClass('active');
        });
    });

    // products view mode
    $(document).on('click', '.products-view-mode > span', function (e) {
        e.preventDefault();
        if ($(this).hasClass('products-view-mode-active')) {
            return false;
        } else {
            $('.products-view-mode > span').removeClass('products-view-mode-active');
            $(this).addClass('products-view-mode-active');
            if ($(this).hasClass('products-view-mode-grid')) {

                $('#products-cont').removeClass('view-mode-list');
                $('#products-cont-pod').removeClass('view-mode-list');
                $('#products-cont-sub').removeClass('view-mode-list');


            } else if ($(this).hasClass('products-view-mode-list')) {

                $('#products-cont').addClass('view-mode-list');
                $('#products-cont-pod').addClass('view-mode-list');
                $('#products-cont-sub').addClass('view-mode-list');
            }
        }
    });

    $('#boxxx label').attr('class', 'checkbox-design align-items-center')
    $('#boxxx label input').after('<span class="checkbox-square"></span>')

    $(document).on('click', '.pgs', function (event) {
        let qparam
        const page = event.target.dataset.page
        
        if (!window.location.search.length) {
            qparam = new URLSearchParams(`page=${page}`)
            
        } else {
            
            if(!(new URLSearchParams(window.location.search)).has('page')){
                qparam = new URLSearchParams(window.location.search + `&page=${page}`)
            }else{
                qparam = new URLSearchParams(window.location.search)
                qparam.set('page',`${page}`)
                
                console.log(qparam.toString())
            }
        }
        window.location.replace(window.location.origin + window.location.pathname + `?${qparam.toString()}`)
        console.log(qparam.toString())
    })
    

});
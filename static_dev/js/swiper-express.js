$(document).ready(function () {

// Main slider
$(function () {
    var swiper = new Swiper('.main-slide', {
       pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
});

// Main product
$(function () {
 var swiper = new Swiper('.slider-4 ', {
      slidesPerView: 4,
      spaceBetween: 16,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {
		  300: {
          slidesPerView: 1,
          spaceBetween: 16,
        },
        567: {
          slidesPerView: 2,
          spaceBetween: 16,
        },
        991: {
          slidesPerView: 3,
          spaceBetween: 16,
        },
        1145: {
          slidesPerView: 4,
          spaceBetween: 16,
        },
      }
    });
});

// Gallery Thumb
$( function() {
 var galleryThumbs = new Swiper('.gallery-thumbs', {
      spaceBetween: 5,
      slidesPerView: 4,
      watchSlidesVisibility: true,
      watchSlidesProgress: true,
    });
    var galleryTop = new Swiper('.gallery-top', {
      spaceBetween: 10,
		centeredSlides: true,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      thumbs: {
        swiper: galleryThumbs
      }
    });
	});
	
});	
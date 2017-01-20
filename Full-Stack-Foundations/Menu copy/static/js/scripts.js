(function($){
	"use strict";


	$('[data-bg-image]').each(function(){
		$(this).css({ 'background-image': 'url('+$(this).data('bg-image')+')' });
	});

	$('[data-bg-color]').each(function(){
		$(this).css({ 'background-color': $(this).data('bg-color') });
	});

	$('[data-width]').each(function(){
		$(this).css({ 'width': $(this).data('width') });
	});

	$('[data-height]').each(function(){
		$(this).css({ 'height': $(this).data('height') });
	});

	$('[data-alpha]').each(function(){
		$(this).css({ 'opacity': $(this).data('alpha') });
	});



	// header search action
	$('#header-search').on('click', function(){
		$('#overlay-search').addClass('active');

		setTimeout(function(){
			$('#overlay-search').find('input').eq(0).focus();
		}, 400);
	});
	$('#overlay-search').find('.close-search').on('click', function(){
		$('#overlay-search').removeClass('active');
	});


	// mobile menu
	$('nav.main-nav').on('click', function(){
		if( $(window).width()<997 ){
			$('nav.main-nav').addClass('show-menu');
		}
	});
	$('#close-menu').on('click', function(){
		$('nav.main-nav.show-menu').removeClass('show-menu');
		return false;
	});


	$('.mouse-wheel').each(function(){
		var $mw = $(this);
		$mw.on('click', function(){
			$('html,body').animate({
				scrollTop: $mw.offset().top + 44 + 30
			});
		});
	});



	$('.fullwidth-tabs').each(function(){
		var $tab = $(this);

		if( !$tab.find('.tabs-nav li.active').length ){
			$tab.find('.tabs-nav li').eq(0).addClass('active');
		}

		var _current = $tab.find('.tabs-nav li').index($tab.find('.tabs-nav li.active'));

		$tab.find('.tabs-contents .tabs-content').eq(_current).slideDown();

		$tab.find('.tabs-nav li a').on('click', function(){
			var current_index = $tab.find('.tabs-nav li').index($(this).parent());
			$tab.find('.tabs-nav li').removeClass('active');
			$(this).parent().addClass('active');
			$tab.find('.tabs-contents .tabs-content').slideUp();
			$tab.find('.tabs-contents .tabs-content').eq(current_index).slideDown();
		});

	});


	$(document).ready(function(){

		// Sticky menu execution
		if( $('body').hasClass('sticky-menu') ) {

			var headerBottom = $('#header').offset().top + $('#header').height();

			var lastScrollTop = 0;
			$(window).scroll(function(event){
				var st = $(this).scrollTop();

				if( $(window).width()<992 ){
					if (st > lastScrollTop){
						// downscroll code
						$("body").removeClass("stick");
					} else {
						// upscroll code
						$("body").addClass("stick");
					}
				}
				else{
					if (st >= headerBottom ) {
				        $("body").addClass("stick");
				    } else {
				    	$("body").removeClass("stick");
				    }
				}
				if( st == 0 ) {
					$("body").removeClass("stick");
				}
				lastScrollTop = st;
			});

		}

		// Gallery slideshow
		$('.gallery-slideshow').each(function(){
			var _gallery = $(this);

			_gallery.find('.gallery-container').swiper({
			    nextButton: _gallery.find('.swiper-button-next'),
			    prevButton: _gallery.find('.swiper-button-prev')
			});
		});


		// Video Element
		$('.video-element').each(function(){
			var _video = $(this);
			_video.magnificPopup({
				delegate: 'a',
				type: 'iframe'
			});
		});

		
		$('.image-link').each(function(){
			var $this = $(this);
			$this.magnificPopup({
				type:'image'
			});
		});


		// carousel slider
		$('.carousel-posts').each(function(){
			var $this = $(this);
			$this.find('.swiper-container').swiper({
				loop: true,
				slidesPerView: 3,
				centeredSlides: true,
				initialSlide: 1,
				nextButton: $this.find('.swiper-button-next'),
			    prevButton: $this.find('.swiper-button-prev'),
			    breakpoints: {
			    	996: {
			    		slidesPerView: 2
			    	}
			    }
			});
		});


		$('.team-carousel').each(function(){
			var $this = $(this);
			$this.find('.swiper-container').swiper({
				loop: true,
				slidesPerView: 3,
				centeredSlides: true,
				pagination: $this.find('.swiper-pagination'),
			    breakpoints: {
			    	996: {
			    		slidesPerView: 2
			    	},
			    	600: {
			    		slidesPerView: 1
			    	}
			    }
			});
		});



		$('.clients-carousel').each(function(){
			var $this = $(this);
			$this.find('.swiper-container').swiper({
				loop: true,
				slidesPerView: 5,
				centeredSlides: true,
				pagination: $this.find('.swiper-pagination'),
			    breakpoints: {
			    	996: {
			    		slidesPerView: 4
			    	},
			    	600: {
			    		slidesPerView: 2
			    	}
			    }
			});
		});



		$('.chefs-carousel').each(function(){
			var $this = $(this);
			$this.find('.swiper-container').swiper({
				slidesPerView: 4,
				pagination: $this.find('.swiper-pagination'),
			    breakpoints: {
			    	996: {
			    		slidesPerView: 3
			    	},
			    	600: {
			    		slidesPerView: 1
			    	}
			    }
			});
		});


		// fullwidth post slider
		$('.fullwidth-post-slider').each(function(){
			var $this = $(this);
			$this.find('.swiper-container').swiper({
				nextButton: $this.find('.swiper-button-next'),
			    prevButton: $this.find('.swiper-button-prev'),
			    pagination: $this.find('.swiper-pagination'),
			    paginationClickable: true
			});
		});



		//
		$('.carousel-container').each(function(){
			var $this = $(this);
			var _col = parseInt($this.data('col'), 10);

			if( _col>0 ){
				$this.swiper({
					nextButton: $this.find('.swiper-button-next'),
				    prevButton: $this.find('.swiper-button-prev'),
				    pagination: $this.find('.swiper-pagination'),
				    paginationClickable: true,
				    slidesPerView: _col,
				    breakpoints: {
				    	996: {
				    		slidesPerView: 5
				    	},
				    	600: {
				    		slidesPerView: 3
				    	}
				    }
				});
			}
			else{
				$this.swiper({
					nextButton: $this.find('.swiper-button-next'),
				    prevButton: $this.find('.swiper-button-prev'),
				    pagination: $this.find('.swiper-pagination'),
				    paginationClickable: true
				});
			}

		});

	});


	$(window).load(function(){


		$('.portfolio-container.masonry').each(function(){
			var _masonry = $(this);
			var _col_width = _masonry.data('col-width');
			if( _col_width.indexOf('col-')<0 ){
				_col_width = '.col-md-3';
			}

			_masonry.isotope({
				itemSelector: '.masonry-item',
				masonry: {
                    columnWidth: _col_width
                }
			});
		});

		$('.gallery-masonry').each(function(){
			var $this = $(this);

			$this.find('.gallery-viewport').isotope({
				itemSelector: '.gitem',
				masonry: {
                    columnWidth: 1
                }
			});

			$this.find('.gallery-viewport').magnificPopup({
				delegate: '.gitem a',
				type: 'image',
				gallery:{
					enabled:true
				}
			});

		});


		$('.blog-masonry-container').each(function(){
			var $this = $(this);
			$this.isotope({
				itemSelector: '.masonry-item',
				masonry: {
                    columnWidth: 1
                }
			});
		});

	});


})(jQuery);
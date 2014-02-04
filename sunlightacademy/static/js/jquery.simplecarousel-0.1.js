;(function($) {

	$.fn.carousel = function(options) {

		var opts = options || {};
		opts.autoAdvance = opts.autoAdvance || true;

		var next = function(carousel) {
			carousel.find('li:first').animate(
				{width: 0},
				{queue: false, duration: 300, complete: function() {
					carousel.find('ul').append(
						$(this).css(
							{'width': carousel.data('slideWidth')}
						)
					);
				}}
			);
		};

		var previous = function(carousel) {
			carousel.find('ul').prepend(
				carousel.find('li:last').css({'width': 0})
			);
			carousel.find('li:first').animate(
				{width: carousel.data('slideWidth')},
				{queue: false, duration: 300}
			);
		};

		return this.each(function() {

			var elem = $(this);
			var userIntervention = false;
			var slideWidth = elem.find('li').outerWidth();

			elem.data('slideWidth', slideWidth);

			elem.find('ul').css(
				{'width': elem.find('li').length * slideWidth}
			).prepend(
				elem.find('li:last')
			);

			var nextElem = opts.nextElem || elem.find('a.carousel-next');
			nextElem.click(function(ev) {
				next(elem, slideWidth);
				userIntervention = true;
				ev.preventDefault();
			});

			var previousElem = opts.previousElem || elem.find('a.carousel-previous');
			previousElem.click(function(ev) {
				previous(elem, slideWidth);
				userIntervention = true;
				ev.preventDefault();
			});

			if (opts.autoAdvance) {
				var autoAdvance = function() {
					if (userIntervention) {
						return;
					}
					next(elem, slideWidth);
					setTimeout(autoAdvance, 10000);
				};
				setTimeout(autoAdvance, 10000);
			}

		});
	};

})(jQuery);

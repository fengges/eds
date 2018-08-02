
$(function() {
	/**
 	*
 	* accordion
 	*
 	*/
	var Accordion = function(el, multiple) {
		this.el = el || {};
		this.multiple = multiple || false;

		// Variables privadas
		var links = this.el.find('.link');
		// Evento
		links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
	}

	Accordion.prototype.dropdown = function(e) {
		var $el = e.data.el;
		var	$this = $(this);
		var	$next = $this.next();

		$next.slideToggle();
		$this.parent().toggleClass('open');

		if (!e.data.multiple) {
			$el.find('.submenu').not($next).slideUp().parent().removeClass('open');
		};
	}

	var accordion = new Accordion($('.accordion'), false);
//	$("#bg_head").MyFloatingBg({direction:1, speed:2000000});

    var setting = {
        width:1000,
        height:270,
        postWidth:658,
        postHeight:270,
        scale:0.8,
        speed:500,
        verticalAlign:"center"
    }
    $(".carousel").attr("data-setting",'{ "width":900,"height":411,"postWidth":658}')
    Carousel.init($(".carousel"))
});

(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
		if($('.searchbar_base').css('margin-inline-start') == "250px"){ // or this.value == 'volvo'
      		$('.searchbar_base').css('margin-inline-start',"110px");
			}
      	else {
		$('.searchbar_base').css('margin-inline-start', "250px");
			}

  });

})(jQuery);

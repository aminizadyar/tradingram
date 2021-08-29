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

		if($('.invisible_behind_sidebar').css('display') == "none"){ // or this.value == 'volvo'
      		$('.invisible_behind_sidebar').css('display','block');
			}
      	else {
		$('.invisible_behind_sidebar').css('display','none');
			}

		if($('.searchbar_base').css('margin-inline-start') == "250px"){ // or this.value == 'volvo'
      		$('.searchbar_base').css('margin-inline-start',"110px");
			}
      	else {
		$('.searchbar_base').css('margin-inline-start', "250px");
			}

  });

})(jQuery);



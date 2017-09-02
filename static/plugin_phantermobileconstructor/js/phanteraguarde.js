(function($, undefined) { 
	$.fn.aguarde = function(){
		$(this).html('<div class="caixa_aguarde"><div id="aguarde">&#160;</div></div>');
		$("#aguarde").animateSprite({
		          fps: 25,
		          animations: {
		              walkRight: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
		          },
		          loop: true,
		          complete: function(){
		              // use complete only when you set animations with 'loop: false'
		              alert("animation End");
		          }
		});				
	}
})(jQuery);

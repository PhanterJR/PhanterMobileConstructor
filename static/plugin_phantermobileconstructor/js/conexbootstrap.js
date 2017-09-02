(function($, undefined) {
	var viewportWidth = $(window).width();
	var viewportHeight = $(window).height();
	var viewportType = "responsivo"
	var flash_principal=$(".flash_principal")
	$(document).ready(function(){
		$('.conex_principal').height(viewportHeight-220);
	}) 


	$.fn.refresh_viewport = function(){
		viewportWidth = $(window).width();
		viewportHeight = $(window).height();
		if (viewportWidth<350){
			mudar_viewport('phone')
		} else if (viewportWidth>349 & viewportWidth<450){
			mudar_viewport('phonelg')
		} else if (viewportWidth>449 & viewportWidth<600){
			mudar_viewport('tablet')
		} else if (viewportWidth>599 & viewportWidth<1024){
			mudar_viewport('desktop')
		} else if (viewportWidth>1023){
			mudar_viewport('desktoplg')
		}
	};


	$(function(){
		viewportWidth = $(window).width();
		viewportHeight = $(window).height();
		
		if (viewportWidth<350){
			mudar_viewport('phone')
		} else if (viewportWidth>349 & viewportWidth<450){
			mudar_viewport('phonelg')		
		} else if (viewportWidth>449 & viewportWidth<600){
			mudar_viewport('tablet')
		} else if (viewportWidth>599 & viewportWidth<1024){
			mudar_viewport('desktop')
		} else if (viewportWidth>1023){
			mudar_viewport('desktoplg')
		}
		flash_principal.fadeIn(1000).delay(50000).fadeOut(1000);
	})
	$(function(){
	
		flash_principal.click(function(){
			flash_principal.fadeOut()
		});
		$("#cobra_principal").animateSprite({
		      fps: 9,
		      animations: {
		          walkRight: [0, 0, 0, 0, 0, 0, 7, 0, 1, 2, 1, 2, 1, 0, 0, 0, 0, 3, 4, 3, 0, 5, 6, 5, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 0, 0, 0, 8, 9, 10, 10, 10, 10, 10, 10, 9, 8, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 0, 0, 0, 7, 15, 14, 14, 11, 12, 11, 12, 11, 14, 14, 14, 13, 14, 13, 14, 14, 15, 7, 0, 0, 0, 0 ]
		      },
		      loop: true,
		      complete: function(){
		          // use complete only when you set animations with 'loop: false'
		          alert("animation End");
		      }
		  });
		  $("#cobra_secundaria").animateSprite({
		      fps: 9,
		      animations: {
		          walkRight: [0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 2,3,2,1,0, 0, 0, 0, 0, 0, 1, 2, 4, 5, 6, 2,3,2,1,0 ,7,0,7, 0,0,0,7,0,0,12,13,11,10,9,8,8,8,8,8,8,8,8,8,8,8,8,9,10,11,13,12,0,0,0,7,0,7,15,14,15,7,0,0,0,7,0,7]
		      },
		      loop: true,
		      complete: function(){
		          // use complete only when you set animations with 'loop: false'
		          alert("animation End");
		      }
		  });   
	})
	$(function(){
	var target = location.hash.replace("#_","#") && $(location.hash.replace("#_","#"))[0];

	if(target)
	    $('html,body').animate({scrollTop:$(target).offset().top-70}, 1400);
	    //$.scrollTo( target, {speed:5000} );
	});  
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
function aguarde (id_alvo) {
	$(id_alvo).html('<div class="caixa_aguarde"><div id="aguarde">&#160;</div></div>');
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
};

var viewportWidth = $(window).width();
var viewportHeight = $(window).height();
var viewportType = "responsivo"
function mudar_viewport(responsivo){
	var responsivo=responsivo
	$(".responsivo").each(function(){
		if (responsivo=='desktop'){
			$(this).removeClass("responsivo-phone").removeClass("responsivo-tablet").removeClass("responsivo-desktoplg").removeClass("responsivo-phonelg");
			$(this).addClass("responsivo-desktop");
		} else if (responsivo=='phone'){
			$(this).removeClass("responsivo-desktop").removeClass("responsivo-tablet").removeClass("responsivo-desktoplg").removeClass("responsivo-phonelg");
			$(this).addClass("responsivo-phone");					
		} else if (responsivo=='phonelg'){
			$(this).removeClass("responsivo-phone").removeClass("responsivo-desktop").removeClass("responsivo-tablet").removeClass("responsivo-desktoplg");
			$(this).addClass("responsivo-phonelg");					
		} else if (responsivo=='tablet'){
			$(this).removeClass("responsivo-phone").removeClass("responsivo-desktop").removeClass("responsivo-desktoplg").removeClass("responsivo-phonelg");
			$(this).addClass("responsivo-tablet");						
		} else if (responsivo=='desktoplg'){
			$(this).removeClass("responsivo-phone").removeClass("responsivo-tablet").removeClass("responsivo-desktop").removeClass("responsivo-phonelg");
			$(this).addClass("responsivo-desktoplg");					
		}	
	});
}
$('.conex_principal').css('height', viewportHeight-220)
	$(window).resize(function() {
		viewportWidth = $(window).width();
		viewportHeight = $(window).height();
		$('.conex_principal').css('height', viewportHeight-220)
		if (viewportWidth<350){
			if (viewportType!="phone"){
				viewportType="phone"
				mudar_viewport('phone')
				
			}
		} else if (viewportWidth>349 & viewportWidth<450){
			if (viewportType!="phonelg"){
				viewportType="phonelg"
				mudar_viewport('phonelg')
				
			}	
		} else if (viewportWidth>449 & viewportWidth<600){
			if (viewportType!="tablet"){
				viewportType="tablet"
				mudar_viewport('tablet')
				
			}	
		} else if (viewportWidth>599 & viewportWidth<1024){
			if (viewportType!="desktop"){
				viewportType="desktop"
				mudar_viewport('desktop')
				
			}			
		} else if (viewportWidth>1023){
			if (viewportType!="desktoplg"){
				viewportType="desktoplg"
				mudar_viewport('desktoplg')
			}
		}
	});
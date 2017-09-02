
$(document).ready(function(){
	var altura_janela=$(window).height()
	//Blog
	$(".mostrar_comentarios_blog_artigo").click(function(){
		var alvo=$(this).attr('alvo');
		$('#caixa_ajax_comentarios_'+alvo).aguarde();
		url_echo='/conexaodidata/blog/echo_comentarios/'+alvo
		ajax(url_echo,[], ':eval');
		$(this).hide();
		$('#ocultar_comentarios_blog_artigo_'+alvo).show();
	});
	//------------------------------
	//Página Principal
	$('.conex_principal').height(altura_janela-220);
	//------------------------------
	//Topo
	if ($(window).scrollTop()>=200){
		var mudar_briba=true
		$('#cobra_principal').removeClass('phantersprit_cobra_principal cobra_principal').addClass('scroll phantersprit_cobratopo cobratopo');
	}else{
		var mudar_briba=false
		$('#cobra_principal').removeClass('scroll phantersprit_cobratopo cobratopo').addClass('phantersprit_cobra_principal cobra_principal');
	}
	
    $(window).scroll(function() {
    	altura_janela=$(window).height()
        var posicao_scroll=$(window).scrollTop()
        var posicao_divfinal=$('#final').position().top
        var porcentagem_scroll=Math.round(posicao_scroll/(posicao_divfinal-altura_janela)*100)
        //$('body').css('background-position-y', posicao_scroll/100 + 'px');
        //$('#paralax-painel').css('height', posicao_scroll/2 + 'px');

		if ($(window).scrollTop()>=200 && mudar_briba==true){
			mudar_briba=false
			$('#cobra_principal').removeClass('phantersprit_cobra_principal cobra_principal').addClass('scroll phantersprit_cobratopo cobratopo');
			$('.phanterpainel_caixaprincipal.responsivo-tabletlg').addClass('painel_scroll');
			$('.phanterpainel_caixaprincipal.responsivo-tablet').addClass('painel_scroll');
			$('.phanterpainel_caixaprincipal.responsivo-phone').addClass('painel_scroll');
			$('.phanterpainel_caixaprincipal.responsivo-phonelg').addClass('painel_scroll');
			$(".scroll").click(function(){
				mudar_briba=false
			      var ancora=$(this).attr('ancora')
			      console.log(ancora);
			      $('html,body').animate({scrollTop:$(ancora).offset().top-100}, 1400);
			      $(this).unbind();
			 });
		} else if ($(window).scrollTop()<200 && mudar_briba==false){
			mudar_briba=true
			$(".scroll").unbind();
			$('.phanterpainel_caixaprincipal.responsivo-tabletlg').removeClass('painel_scroll');
			$('.phanterpainel_caixaprincipal.responsivo-tablet').removeClass('painel_scroll');
			$('.phanterpainel_caixaprincipal.responsivo-phone').removeClass('painel_scroll');
			$('.phanterpainel_caixaprincipal.responsivo-phonelg').removeClass('painel_scroll');
			$('#cobra_principal').removeClass('scroll phantersprit_cobratopo cobratopo').addClass('phantersprit_cobra_principal cobra_principal');
		};
      
    });
    //Scroll click;
    $(".scroll").click(function(event){
          event.preventDefault();
          var ancora=$(this).attr('ancora')
          console.log(ancora);
          $('html,body').animate({scrollTop:$(ancora).offset().top-100}, 1400);
     });
    //Ancora na url
    $(function(){
		var target = $(location.hash.replace("#_","#"))[0];
		if(target)
		    $('html,body').animate({scrollTop:$(target).offset().top-70}, 1400);
	});
	//Painel direito
	var estado_painel=true
	$(".phanterpainel_botao").click(function(){
		if (estado_painel==true){
			estado_painel=false
			$(this).addClass("div_float");
			$('.phanterpainel_caixapainel.responsivo-tablet').css('display', 'block').unbind();
			$('.phanterpainel_caixapainel.responsivo-tabletlg').css('display', 'block').unbind();
			$('.phanterpainel_caixapainel.responsivo-phone').css('display', 'block').unbind();
			$('.phanterpainel_caixapainel.responsivo-phonelg').css('display', 'block').unbind();
		} else{
			estado_painel=true
			$(this).removeClass("div_float");
			$('.phanterpainel_caixapainel.responsivo-tablet').css('display', 'none').unbind();
			$('.phanterpainel_caixapainel.responsivo-tabletlg').css('display', 'none').unbind();
			$('.phanterpainel_caixapainel.responsivo-phone').css('display', 'none').unbind();
			$('.phanterpainel_caixapainel.responsivo-phonelg').css('display', 'none').unbind();
		}

	});
})

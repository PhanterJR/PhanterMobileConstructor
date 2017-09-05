var estado_menu_principal=false; 
$(".botao_hamburguer").click(function(){
  var alvo=$(this).attr("alvo"); 
  console.log(estado_menu_principal);
  if(estado_menu_principal==false){
    estado_menu_principal=true; $(alvo).slideDown(); $(this).css('background', '#000000b3');
  } else {
    estado_menu_principal=false; $(alvo).slideUp(); $(this).css('background', 'none')};
  });

$(".phantermobile-botao-ajax").click(function(){
	var url_ajax=$(this).attr('url_ajax');
  console.log(url_ajax)
  var alvo=$(this).attr('alvo');
  if (url_ajax!=null||url_ajax!=undefined){
    $(alvo).html('<i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>');
    ajax(url_ajax,[],':eval');
  }
});
$(".phantermobile-botao-href").click(function(){
	var url_href=$(this).attr('url_href');
	window.location=url_href
});

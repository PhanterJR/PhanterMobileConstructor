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
	ajax(url_ajax,[],':eval');
});
$(".phantermobile-botao-href").click(function(){
	var url_href=$(this).attr('url_href');
	window.location=url_href
});

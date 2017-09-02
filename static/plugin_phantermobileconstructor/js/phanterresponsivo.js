phanterresponsivo={
	phanterclasschavepadrao:'responsivo',
	phanterestadoatual:'default',
	phanterviewsizes:[],
	phanterviewports:function(nome, tamanho_inicial, tamanho_final, classchave){
		 classchave = classchave || this.phanterclasschavepadrao;
		this.phanterviewsizes.push([nome, tamanho_inicial, tamanho_final, classchave]);
		return this.phanterviewsizes
	},
	phanterresponsivo:function(){
		var viewportWidth = $(window).width();
		var viewportHeight = $(window).height();
		var phanterviewsizes=this.phanterviewsizes
		var classes_retirar=[]
		var classe_colocar=''
		var classchave=this.phanterclasschavepadrao
		for(var x in phanterviewsizes){
			classchave=phanterviewsizes[x][3]
			var nome_class=classchave+'-'+phanterviewsizes[x][0]
			var tamanho_inicial=phanterviewsizes[x][1]
			var tamanho_final=phanterviewsizes[x][2]
			if (viewportWidth>=tamanho_inicial && viewportWidth<tamanho_final){
				classe_colocar=nome_class
			} else {
				classes_retirar.push(nome_class)
			}
		}
		$("."+classchave).each(function(){
			for(var y in classes_retirar){
				$(this).removeClass(classes_retirar[y])
				$(this).removeClass("landscape")
				$(this).removeClass("portrait")
			};
			$(this).addClass(classe_colocar)
			if (viewportWidth>viewportHeight){
				$(this).addClass("landscape")
			} else {
				$(this).addClass("portrait")
			}
		});
	}
}
phanterresponsivo.phanterviewports('phone', 0, 350, 'responsivo')
phanterresponsivo.phanterviewports('phonelg', 350, 450, 'responsivo')
phanterresponsivo.phanterviewports('tablet', 450, 600, 'responsivo')
phanterresponsivo.phanterviewports('tabletlg', 600, 800, 'responsivo')
phanterresponsivo.phanterviewports('desktop', 800, 1024, 'responsivo')
phanterresponsivo.phanterviewports('desktoplg', 1024, 10000, 'responsivo')
$(document).ready(function(){
	phanterresponsivo.phanterresponsivo();
})
$(window).resize(function(){
	phanterresponsivo.phanterresponsivo();
})
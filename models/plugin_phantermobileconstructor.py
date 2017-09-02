# -*- coding: utf-8 -*-
from plugin_phantermobileconstructor.phantermenubar import PhanterMenubar
import os
import urllib2

response.barra_ferramentas=""
if request.vars.phantermobilebuild:
    response.servidor_ajax = "http://192.168.1.107:%s/%s/" %(request.env.server_port,request.application)
else:
    response.barra_ferramentas=DIV(
        DIV('Ferramentas', 
            _class='botao_response_toolbar', 
            _style='cursor:pointer; position: fixed;right: 0; bottom: 145px; width: 93px; padding: 5px; background-color: orange; text-transform: uppercase; font-weight: bold;font-size: 8pt;padding-left: 10px;box-shadow: -1px 2px 3px;', 
            _onclick='$("#caixa_response_toolbar").toggle();'), 
        DIV(response.toolbar(), 
            _id='caixa_response_toolbar', 
            _style='background-color:white; padding:5px; display:none;'), 
        _style='position:relative; z-index:1005; width:100%;')
    response.servidor_ajax = "http://127.0.0.1:%s/%s/" %(request.env.server_port,request.application)
if request.controller=='plugin_phantermobileconstructor':

    lista_links=[DIV(DIV(I(_class="glyphicon glyphicon-menu-hamburger"), _alvo=".grupo_links", _class='botao_hamburguer responsivo'),
        DIV(A(DIV(XML("&#160;"),_class='botao_conexao responsivo'), _href=URL('phantermobileconstructor', 'index')),
        A(DIV("Admin", _class='menu_item responsivo'), _href=URL('admin', 'default', 'index')),
        A(DIV("index", _class='menu_item responsivo'), _href=URL('plugin_phantermobileconstructor', 'www_index')),
        DIV(DIV("compilar", _class='menu_item responsivo'), _class="phantermobile-botao-ajax", _url_ajax=URL('phantermobileconstructor', 'build')),
        DIV(DIV("resetar", _class='menu_item responsivo'), _class="botao_ajax", _comando='resetar', _url_ajax=URL('phantermobileconstructor', 'reset')),
        A(DIV("configurações", _class='menu_item responsivo'), _href=URL('default', 'configuracoes')),
        _class='grupo_links responsivo')),
        ]
    response.menu_principal = PhanterMenubar(*lista_links, _class="barra_navegacao responsivo")
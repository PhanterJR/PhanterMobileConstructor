# -*- coding: utf-8 -*-
from plugin_phantermobileconstructor.phantermenubar import PhanterMenubar
import os
import urllib2

response.toolbar_mob = ""
if request.vars.phantermobilebuild:
    response.ajax_server = "http://192.168.1.107:%s/%s/" % (
        request.env.server_port, request.application)
else:
    response.toolbar_mob = DIV(
        DIV(A(T('Web2py ToolBar'), _style="color: #440808;", _href="#caixa_response_toolbar"),
            _class='botao_response_toolbar',
            _style='cursor:pointer; position: fixed;right: 0; bottom: 45px; width: 93px; padding: 5px; background-color: orange; text-transform: uppercase; font-weight: bold;font-size: 8pt;padding-left: 10px;box-shadow: -1px 2px 3px black;',
            _onclick='$("#caixa_response_toolbar").toggle();'),
        DIV(response.toolbar(),
            _id='caixa_response_toolbar',
            _style='background-color:white; padding:5px; display:none;'),
        _style='position:relative; z-index:1005; width:100%;')
    response.ajax_server = "http://127.0.0.1:%s/%s/" % (
        request.env.server_port, request.application)
if request.controller == 'plugin_phantermobileconstructor':

    lista_links = [DIV(DIV(I(_class="glyphicon glyphicon-menu-hamburger"), _alvo=".grupo_links", _class='botao_hamburguer responsivo'),
                       DIV(A(DIV(XML("&#160;"), _class='botao_conexao responsivo'), _href=URL('phantermobileconstructor', 'index')),
                           A(DIV("Admin", _class='menu_item responsivo'),
                             _href=URL('admin', 'default', 'index')),
                           A(DIV("index", _class='menu_item responsivo'), _href=URL(
                               'plugin_phantermobileconstructor', 'www_index')),
                           DIV(DIV("compilar", _class='menu_item responsivo'), _class="phantermobile-botao-ajax",
                               _url_ajax=URL('phantermobileconstructor', 'build')),
                           DIV(DIV("resetar", _class='menu_item responsivo'), _class="botao_ajax",
                               _comando='resetar', _url_ajax=URL('phantermobileconstructor', 'reset')),
                           A(DIV("configurações", _class='menu_item responsivo'),
                             _href=URL('default', 'configuracoes')),
                           _class='grupo_links responsivo')),
                   ]
    response.nav_phantermenubar = PhanterMenubar(
        *lista_links, _class="barra_navegacao responsivo")

# Storage APKs

db.define_table('plugin_phantermobileconstructor_apks',
      Field('appname', 'string', label='Name of App'),
      Field('apkfile','upload', autodelete=True),
      Field('apkversion', 'string', label='Version'),
      Field('apklevel', 'string', default='debug')
      )

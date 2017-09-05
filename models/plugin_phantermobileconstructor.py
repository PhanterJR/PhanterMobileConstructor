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
                       DIV(A(DIV(XML("&#160;"), _class='botao_conexao responsivo'), _href="http://www.conexaodidata.com.br"),
                           A(DIV("PhanterMobile Constructor", _class='menu_item responsivo'),
                             _href=URL('plugin_phantermobileconstructor', 'index')),
                           A(DIV("Admin", _class='menu_item responsivo'),
                             _href=URL('admin', 'default', 'index')),
                           A(DIV("Appadmin", _class='menu_item responsivo'), _href=URL(
                               'appadmin', 'index')),
                           _class='grupo_links responsivo')),
                   ]
    response.nav_phantermenubar = PhanterMenubar(
        *lista_links, _class="barra_navegacao responsivo")


# Storage APKs and app info

db.define_table('plugin_phantermobileconstructor_apks',
      Field('appname', 'string', default=request.application, label=T('App Name'), requires=IS_NOT_EMPTY()),
      Field('idapp', 'string', 
        default="com.yoursite.%s" %request.application, 
        label=CAT(T('ID'), SPAN(" ?", _title=T("Specifies the app's reverse-domain identifier, and the version its full version number expressed in major/minor/patch notation."))),
        requires=IS_NOT_EMPTY()
        ),
      Field('apkversion', 'string', 
        default="0.0.1",
        label=CAT(T('Version'), SPAN(" ?", _title=T("Full version number expressed in major/minor/patch notation."))),
        requires=IS_NOT_EMPTY()
        ),
      Field('authorname', 'string', 
        default="PhanterMobile", 
        label=CAT(T('Name of the author'), SPAN(" ?", _title=T("Name that may appear within app-store lisitngs."))),
        requires=IS_NOT_EMPTY()
        ),
      Field('authoremail', 'string', 
        default="contato@conexaodidata.com.br", 
        label=CAT(T('Email of the author'), SPAN(" ?", _title=T("Email that may appear within app-store lisitngs."))),
        requires=[IS_NOT_EMPTY(), IS_EMAIL()]
        ),
      Field('authorwebsite', 'string', 
        default="http://conexaodidata.com.br/phantermobileconstructor", 
        label=CAT(T('Website of the author'), SPAN(" ?", _title=T("Website that may appear within app-store lisitngs."))),
        requires=IS_NOT_EMPTY()
        ),
      Field('externalacess', 'list:string', 
        default=["*"], 
        label=CAT(T('Access origin'), SPAN(" ?", _title=T("Defines the set of external domains the app is allowed to communicate with."))),
        requires=IS_NOT_EMPTY()
        ),
      Field('allownavigation', 'list:string', 
        label=CAT(T('Allow Navigation'), SPAN(" ?", _title=T("Defines the set of external domains the WebView is allowed to navigate to."))),
        ),
      Field('allowintent', 'list:string', 
        default=["http://*/*", "https://*/*", "tel:*", "sms:*", "mailto:*", "geo:*" ],
        label=CAT(T('Allow-Intent'), SPAN(" ?", _title=T("Defines which URLs the app is allowed to ask the system to open."))),
        requires=IS_NOT_EMPTY()
        ),
      Field('apklevel', 'string', default='debug', 
        label=CAT(T('Build type'), SPAN(" ?", _title=T("Perform a release build or Perform a debug build"))),
        requires=IS_IN_SET(['debug', 'release'])),
      Field('apkfile','upload', autodelete=True),
      )

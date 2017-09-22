# -*- coding: utf-8 -*-
# phanterandroid defined in models
# python 3 comtability
from __future__ import print_function

import os
import shutil
import gluon.fileutils
from plugin_phantermobileconstructor.phanterparseconfigxml import parseConfigXML

http_host = request.env.http_host.split(':')[0]
remote_addr = request.env.remote_addr
try:
    hosts = (http_host, socket.gethostname(),
             socket.gethostbyname(http_host),
             '::1', '127.0.0.1', '::ffff:127.0.0.1')
except:
    hosts = (http_host, )

if (remote_addr not in hosts) and (remote_addr != "127.0.0.1"):
    raise HTTP(200, T('PhanterMobile Constructor only works locally'))
precisa_autorizacao = ['index', 'echo_comand']

if (request.function in precisa_autorizacao):
    if not gluon.fileutils.check_credentials(request):
        redirect(URL('admin', 'default', 'index',
                     vars=dict(send=URL(args=request.args, vars=request.vars))))

def index():
    
    q_config = None
    if db(db.plugin_phantermobileconstructor_apps).isempty():
        appname, version, idapp = request.application, '0.0.1', 'com.yoursite.yourapp'
    else:
        q_config = db(db.plugin_phantermobileconstructor_apps).select().first()
        appname, version, idapp = q_config.appname, q_config.apkversion, q_config.idapp

    if request.args(0) == 'phonegap':

        phanterandroid.openServer()
        response.server_phonegap_http_address="http://%s:%s/" % (http_host, phanterandroid.port)
        html = DIV(
            DIV(
                DIV(
                    DIV(
                        IFRAME(_src=response.server_phonegap_http_address,
                               _class='iframe_mobile_portrait responsivo'),
                        _class='html_mobile_portrait responsivo'),
                    _class="mobile_portrait responsivo"),
                _class="painel_esquerdo_g"),
            DIV(DIV(H1(T('View in PhoneGap Server')), _class='caixa_titulo_painel_direito_g'),
                DIV(
                DIV(
                    IFRAME(_src=response.server_phonegap_http_address,
                           _class='iframe_mobile_landscape responsivo'),
                    _class='html_mobile_landscape responsivo'),
                _class="mobile_landscape responsivo"),
                DIV(
                    A(DIV("Without Distractions", _class='menu_item_extra_buttons'), _href=response.server_phonegap_http_address, _target="_blank"),
                    _class='extra_buttons'),
                _class="painel_direito_g"),
            _class="painel_principal_g caixa_view_semdistracoes_landscape")

    elif request.args(0) == 'cordova':

        phanterandroid.openServer('cordova')
        response.server_cordova_http_address="http://%s:%s/browser/www" % (http_host,
                                                                  phanterandroid.port)
        html = DIV(
            DIV(
                DIV(
                    DIV(
                        IFRAME(_src=response.server_cordova_http_address, _class='iframe_mobile_portrait responsivo'),
                        _class='html_mobile_portrait responsivo'),
                    _class="mobile_portrait responsivo"),
                _class="painel_esquerdo_g"),
            DIV(DIV(H1(T('View in Cordova Server')), _class='caixa_titulo_painel_direito_g'),
                DIV(
                DIV(
                    IFRAME(_src=response.server_cordova_http_address, _class='iframe_mobile_landscape responsivo'),
                    _class='html_mobile_landscape responsivo'),
                _class="mobile_landscape responsivo"),
                DIV(
                    A(DIV("Without Distractions", _class='menu_item_extra_buttons'), _href=response.server_cordova_http_address, _target="_blank"),
                    _class='extra_buttons'),
                _class="painel_direito_g"),
            _class="painel_principal_g caixa_view_semdistracoes_landscape")
    elif request.args(0) == 'localview':
        if phanterandroid.default_controller:
            controller_default = '%s/index' %phanterandroid.default_controller
        else:
            controller_default = 'plugin_phantermobileconstructor/www_index'

        html = DIV(
            DIV(
                DIV(
                    DIV(
                        IFRAME(_src="http://%s/%s/%s" % (
                        request.env.http_host, request.application, controller_default), _class='iframe_mobile_portrait responsivo'),
                        _class='html_mobile_portrait responsivo'),
                    _class="mobile_portrait responsivo"),
                _class="painel_esquerdo_g"),
            DIV(DIV(H1(T('View in Web2py Server')), _class='caixa_titulo_painel_direito_g'),
                DIV(
                DIV(
                    IFRAME(_src="http://%s/%s/%s" % (
                        request.env.http_host, request.application, controller_default), _class='iframe_mobile_landscape responsivo'),
                    _class='html_mobile_landscape responsivo'),
                _class="mobile_landscape responsivo"),
                DIV(
                    A(DIV("Without Distractions", _class='menu_item_extra_buttons'), _href=URL('www', 'index'), _target="_blank"),
                    _class='extra_buttons'),
                _class="painel_direito_g"),
            _class="painel_principal_g caixa_view_semdistracoes_landscape")
    else:
        if phanterandroid.default_controller:
            controller_default = '%s/index' %phanterandroid.default_controller
        else:
            controller_default = 'plugin_phantermobileconstructor/www_index'
        if q_config:
            html_apks = DIV(
                DIV(H4('APK List')), _style='width:100%; display:table;text-align:center;')
            for x in db(db.plugin_phantermobileconstructor_apks.application == q_config.id).select():
                html_apks.append(DIV(A(_href=URL('default', 'download', args=[
                                 x.apkfile])), _style='float:left; margin:5px; padding:5px; baranground-color:grey;'))
        html = DIV(
            DIV(
                DIV(
                    DIV(
                        IFRAME(
                            _src="http://%s/%s/%s" % (
                                    request.env.http_host, request.application, controller_default),
                            _class='iframe_mobile_portrait responsivo'),
                        _class='html_mobile_portrait responsivo'),
                    _class="mobile_portrait responsivo"),
                _class='painel_esquerdo_g'),
            DIV(
                DIV(H1('PhanterMobile Constructor'),
                    _class='caixa_titulo_painel_direito_g'),
                DIV(
                    DIV(
                        H3(STRONG('App Name: ', _style='color:orange'), appname, STRONG(' Version: ', _style='color:orange'), version, STRONG(' ID: ', _style='color:orange'), idapp), _style="text-align:center;"),
                    DIV(
                        DIV(
                            DIV(T("Compile html"), _class="center_table_cell"),
                            _alvo="#status_compilar",
                            _url_ajax=URL('plugin_phantermobileconstructor',
                                          'echo_comand', args=['buildhtml']),
                            _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                        DIV(_id="status_compilar", _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Open phonegap server"),
                                _class="center_table_cell"),
                            _alvo="#status_servidor_phonegap",
                            _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=[
                                          'info'], vars={'phonegapstatus': True, 'tryagain': True}),
                            _href=URL(args=['phonegap']),
                            _target="_blank",
                            _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                        DIV(SPAN("Without Status", _style='color:grey;'),
                            _id='status_servidor_phonegap', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Open cordova server"),
                                _class="center_table_cell"),
                            _alvo="#status_servidor_cordova",
                            _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=[
                                          'info'], vars={'cordovastatus': True, 'tryagain': True}),
                            _href=URL(args=['cordova']),
                            _target="_blank",
                            _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                        DIV(SPAN("Without Status", _style='color:grey;'),
                            _id='status_servidor_cordova', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Local View"), _class="center_table_cell"),
                            _href=URL(args=['localview']),
                            _target="_blank",
                            _class='botao_pagina_principal_comandos'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        DIV(DIV(T("Create Debug APK"), _class="center_table_cell"),
                            _alvo="#dowload_newapk_debug",
                            _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=[
                                          'createapk', 'debug']),
                            _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                        DIV(_id="dowload_newapk_debug",
                            _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        DIV(DIV(T("Create Release APK"), _class="center_table_cell"),
                            _alvo="#dowload_newapk_release",
                            _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=[
                                          'createapk', 'release']),
                            _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                        DIV(_id="dowload_newapk_release",
                            _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Config XML"), _class="center_table_cell"),
                            _alvo="#status_config_xml",
                            _href=URL('configxml'),
                            _class='botao_pagina_principal_comandos'),
                        DIV(SPAN("Create first Config.xml", _style='color:red;') if db(db.plugin_phantermobileconstructor_apps).isempty(
                        ) else "", _id='status_config_xml', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Config KeyStore"), _class="center_table_cell"),
                            _alvo="#status_config_keystore",
                            _href=URL('configkeystore'),
                            _class='botao_pagina_principal_comandos'),
                        DIV(SPAN("Config your keystore", _style='color:red;') if db(db.plugin_phantermobileconstructor_keystore).isempty(
                        ) else "", _id='status_config_keystore', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Config Icon"), _class="center_table_cell"),
                            _alvo="#status_config_icon",
                            _href=URL('configicon'),
                            _class='botao_pagina_principal_comandos'),
                        DIV(SPAN("Config your Icon", _style='color:red;') if db(db.plugin_phantermobileconstructor_icon).isempty(
                        ) else "", _id='status_config_icon', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Config Splashscreen"), _class="center_table_cell"),
                            _alvo="#status_config_splash",
                            _href=URL('configsplash'),
                            _class='botao_pagina_principal_comandos'),
                        DIV(SPAN("Config your Splashscreen", _style='color:red;') if db(db.plugin_phantermobileconstructor_splash).isempty(
                        ) else "", _id='status_config_splash', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    DIV(
                        A(
                            DIV(T("Add/Remove Plugins"), _class="center_table_cell"),
                            _alvo="#status_plugins",
                            _href=URL('configplugins'),
                            _class='botao_pagina_principal_comandos'),
                        DIV(SPAN("Config your Plugins", _style='color:red;') if db(db.plugin_phantermobileconstructor_plugins).isempty(
                        ) else "", _id='status_plugins', _class='status_botao_principal'),
                        _class="caixa_botao_ajax_principal",
                        ),
                    _class='caixa_comandos'),
                _class='painel_direito_g'),
            _class='painel_principal_g')
    return locals()

def configplugins():
    q_confplugin = db(db.plugin_phantermobileconstructor_plugins).select().first()
    form = SQLFORM(db.plugin_phantermobileconstructor_plugins,
                   q_confplugin.id if q_confplugin else None, showid=False)
    if form.process().accepted:
        if form.vars.plugin_battery_status:
            phanterandroid.addPlugIn('battery_status')
        else:
            phanterandroid.removePlugIn('battery_status')

        if form.vars.plugin_camera:
            phanterandroid.addPlugIn('camera')
        else:
            phanterandroid.removePlugIn('camera')

        if form.vars.plugin_console:
            phanterandroid.addPlugIn('console')
        else:
            phanterandroid.removePlugIn('console')

        if form.vars.plugin_contacts:
            phanterandroid.addPlugIn('contacts')
        else:
            phanterandroid.removePlugIn('contacts')

        if form.vars.plugin_device:
            phanterandroid.addPlugIn('device')
        else:
            phanterandroid.removePlugIn('device')

        if form.vars.plugin_device_motion:
            phanterandroid.addPlugIn('device_motion')
        else:
            phanterandroid.removePlugIn('device_motion')

        if form.vars.plugin_device_orientation:
            phanterandroid.addPlugIn('device_orientation')
        else:
            phanterandroid.removePlugIn('device_orientation')

        if form.vars.plugin_dialogs:
            phanterandroid.addPlugIn('dialogs')
        else:
            phanterandroid.removePlugIn('dialogs')

        if form.vars.plugin_file:
            phanterandroid.addPlugIn('file')
        else:
            phanterandroid.removePlugIn('file')

        if form.vars.plugin_file_transfer:
            phanterandroid.addPlugIn('file_transfer')
        else:
            phanterandroid.removePlugIn('file_transfer')

        if form.vars.plugin_geolocation:
            phanterandroid.addPlugIn('geolocation')
        else:
            phanterandroid.removePlugIn('geolocation')

        if form.vars.plugin_globalization:
            phanterandroid.addPlugIn('globalization')
        else:
            phanterandroid.removePlugIn('globalization')

        if form.vars.plugin_inappbrowser:
            phanterandroid.addPlugIn('inappbrowser')
        else:
            phanterandroid.removePlugIn('inappbrowser')

        if form.vars.plugin_media:
            phanterandroid.addPlugIn('media')
        else:
            phanterandroid.removePlugIn('media')

        if form.vars.plugin_media_capture:
            phanterandroid.addPlugIn('media_capture')
        else:
            phanterandroid.removePlugIn('media_capture')

        if form.vars.plugin_network_information:
            phanterandroid.addPlugIn('network_information')
        else:
            phanterandroid.removePlugIn('network_information')

        if form.vars.plugin_vibration:
            phanterandroid.addPlugIn('vibration')
        else:
            phanterandroid.removePlugIn('vibration')

        if form.vars.plugin_statusbar:
            phanterandroid.addPlugIn('statusbar')
        else:
            phanterandroid.removePlugIn('statusbar')

        session.flash = "Plugins configured"

    return dict(form=form)

def configxml():
    response.flash = T("Edit config.xml of app")
    q_config = db(db.plugin_phantermobileconstructor_apps).select().first()
    form = SQLFORM(db.plugin_phantermobileconstructor_apps,
                   q_config.id if q_config else None, showid=False)
    if form.process().accepted:
        meuxml = parseConfigXML(os.path.join(
            request.env.web2py_path, 'cordova', request.application, 'config.xml'))
        meuxml.appname = form.vars.appname
        meuxml.description = form.vars.description
        meuxml.authorname = form.vars.authorname
        meuxml.apkversion = form.vars.apkversion
        meuxml.idapp = form.vars.idapp
        meuxml.authoremail = form.vars.authoremail
        meuxml.authorwebsite = form.vars.authorwebsite
        
        if form.vars.externalacess:
            for x in form.vars.externalacess:
                meuxml.addElementRoot('access', 'origin', x)
        else:
            meuxml.removeElementRoot('access', 'origin')

        if form.vars.allownavigation:
            for y in form.vars.allownavigation:
                meuxml.addElementRoot('allow-navigation', 'origin', y)
        else:
            meuxml.removeElementRoot('allow-navigation', 'origin')

        if form.vars.allowintent:
            for z in form.vars.allowintent:
                meuxml.addElementRoot('allow-intent', 'href', z)
        else:
            meuxml.removeElementRoot('allow-intent', 'href')
        meuxml.save()
        session.flash = "config.xml saved!"
        redirect(URL('plugin_phantermobileconstructor', 'index'))
    if form.errors:
        response.flash = T("Problems in form!")
    return dict(form=form)

def configicon():
    q_configicon = db(db.plugin_phantermobileconstructor_icon.icon).select().first()
    form = SQLFORM(db.plugin_phantermobileconstructor_icon,
                   q_configicon.id if q_configicon else None, showid=False)
    if form.process().accepted:
        phanterandroid.createIcon(form.vars.icon)
        session.flash = "Icon Created"
        q_configicon = db(db.plugin_phantermobileconstructor_icon.icon).select().first()
    if not q_configicon:
        ldpi=URL('static','plugin_phantermobileconstructor', args=['images', 'phantermobileico.png'])
        mdpi=URL('static','plugin_phantermobileconstructor', args=['images', 'phantermobileico.png'])
        hdpi=URL('static','plugin_phantermobileconstructor', args=['images', 'phantermobileico.png'])
        xhdpi=URL('static','plugin_phantermobileconstructor', args=['images', 'phantermobileico.png'])
        xxhdpi=URL('static','plugin_phantermobileconstructor', args=['images', 'phantermobileico.png'])
        xxxhdpi=URL('static','plugin_phantermobileconstructor', args=['images', 'phantermobileico.png'])
    else:
        ldpi=URL('default', 'downloas', args=[q_configicon.icon])
        mdpi=URL('default', 'downloas', args=[q_configicon.icon])
        hdpi=URL('default', 'downloas', args=[q_configicon.icon])
        xhdpi=URL('default', 'downloas', args=[q_configicon.icon])
        xxhdpi=URL('default', 'downloas', args=[q_configicon.icon])
        xxxhdpi=URL('default', 'downloas', args=[q_configicon.icon])


    html=DIV(H2('Android icons' ,_class='titulo_amostra_icone'),
        DIV(
            DIV(IMG(_src=ldpi, _class='imagem_amostra_icone'), _class='caixa_imagem_amostra_icone ldpi'),
            DIV(IMG(_src=mdpi, _class='imagem_amostra_icone'), _class='caixa_imagem_amostra_icone mdpi'),
            DIV(IMG(_src=hdpi, _class='imagem_amostra_icone'), _class='caixa_imagem_amostra_icone hdpi'),
            DIV(IMG(_src=xhdpi, _class='imagem_amostra_icone'), _class='caixa_imagem_amostra_icone xhdpi'),
            DIV(IMG(_src=xxhdpi, _class='imagem_amostra_icone'), _class='caixa_imagem_amostra_icone xxhdpi'),
            DIV(IMG(_src=xxxhdpi, _class='imagem_amostra_icone'), _class='caixa_imagem_amostra_icone xxxhdpi'),
            _class='caixa_com_icones'),
        _class='caixa_amostra_icone')
    return dict(form=form, html=html)

def configsplash():

    q_configsplash = db(db.plugin_phantermobileconstructor_splash).select().first()
    portrait_ldpi=URL('static', 'plugin_phantermobileconstructor', args=['images', 'screen-xxxhdpi-portrait.png'])
    landscape_ldpi=URL('static', 'plugin_phantermobileconstructor', args=['images', 'screen-xxxhdpi-landscape.png'])
    if request.args(0)=='portrait':
        form = SQLFORM(db.plugin_phantermobileconstructor_splash,
                       q_configsplash.id if q_configsplash else None, fields=['splash_portrait'], showid=False)
        html=CAT(DIV(
                H1(T('Config the Portrait Splashscreen')), HR(),
            _class="caixa_titulo_painel_direito_g"),
            form, HR(),
            DIV(
                H2('Portrait Splashscreen' ,_class='titulo_amostra_screen'),
                DIV(
                    DIV(IMG(_src=portrait_ldpi, _class='imagem_amostra_screen'), _class='caixa_imagem_amostra_screen portrait_ldpi'),
                    _class='caixa_com_screens'),
                _class='caixa_amostra_screen')
            )
        if form.process().accepted:
            q_configsplash = db(db.plugin_phantermobileconstructor_splash,id==form.vars.id).select().first()
            phanterandroid.createSplash(q_configsplash.splash_portrait, portrait=True)
            session.flash = "Splash Portrait Created"
            redirect(URL())
    elif request.args(0)=='landscape':
        form = SQLFORM(db.plugin_phantermobileconstructor_splash,
                       q_configsplash.id if q_configsplash else None, fields=['splash_landscape'], showid=False)
        html=CAT(DIV(
                H1(T('Config the Landscape Splashscreen')), HR(),
            _class="caixa_titulo_painel_direito_g"),
            form, HR(),
            DIV(
                H2('Landscape Splashscreen' ,_class='titulo_amostra_screen'),
                DIV(
                    DIV(IMG(_src=landscape_ldpi, _class='imagem_amostra_screen'), _class='caixa_imagem_amostra_screen landscape_ldpi'),
                    _class='caixa_com_screens'),
                _class='caixa_amostra_screen')
            )
        if form.process().accepted:
            q_configsplash = db(db.plugin_phantermobileconstructor_splash,id==form.vars.id).select().first()
            phanterandroid.createSplash(q_configsplash.splash_landscape, portrait=False)
            session.flash = "Splash Landscape Created"
            redirect(URL()) 
    else:
        screen_landscape=os.path.join(request.folder, 'static', 'plugin_phantermobileconstructor', 'images', 'screen_landscape.png')
        screen_portrait=os.path.join(request.folder, 'static', 'plugin_phantermobileconstructor', 'images', 'screen_portrait.png')
        if q_configsplash:
            generate_landscape=os.path.join(request.env.web2py_path, 'cordova',request.application, 'res', 
                        'screen','android','screen-xxxhdpi-landscape.png')
            generate_portrait=os.path.join(request.env.web2py_path, 'cordova',request.application, 'res', 
                        'screen','android','screen-xxxhdpi-portrait.png')
            if os.path.exists(generate_landscape) and os.path.exists(generate_portrait):
                if os.path.exists(screen_landscape):
                    os.unlink(screen_landscape)
                if os.path.exists(screen_portrait):
                    os.unlink(screen_portrait)
                shutil.copy(generate_landscape, screen_landscape)
                shutil.copy(generate_portrait, screen_portrait)
        html=CAT(
            DIV(
                H1(T('Config the Splashscreen from project')), HR(),
            _class="caixa_titulo_painel_direito_g"),
            DIV(
                DIV(A(DIV(T("Change Portrait Splashscreen"),_class="botao_define_screen"), _href=URL(args=['portrait'])), _class='organizer_50'),
                DIV(A(DIV(T("Change Landscape Splashscreen"),_class="botao_define_screen"), _href=URL(args=['landscape'])), _class='organizer_50'),
                _class='caixa_botoes_define_screen'),
            DIV(
                H2('Portrait Splashscreen' ,_class='titulo_amostra_screen'),
                DIV(
                    DIV(IMG(_src=portrait_ldpi, _class='imagem_amostra_screen'), _class='caixa_imagem_amostra_screen portrait_ldpi'),
                    _class='caixa_com_screens'),
                HR(),
                H2('Landscape Splashscreen' ,_class='titulo_amostra_screen'),
                DIV(
                    DIV(IMG(_src=landscape_ldpi, _class='imagem_amostra_screen'), _class='caixa_imagem_amostra_screen landscape_ldpi'),
                    _class='caixa_com_screens'),
                _class='caixa_amostra_screen'))
    return dict(html=html)

def configkeystore():
    
    if db(db.plugin_phantermobileconstructor_keystore).isempty():
        db.plugin_phantermobileconstructor_keystore.appkeystore.readable = False
        db.plugin_phantermobileconstructor_keystore.appkeystore.writable = False
        keytool = phanterandroid.requeriments('keytool')

        if keytool['keytool']:
            if len(keytool['keytool']) > 1:
                db.plugin_phantermobileconstructor_keystore.keytool.default = keytool[
                    'keytool'][0]
                db.plugin_phantermobileconstructor_keystore.keytool.requires = IS_IN_SET(keytool[
                                                                                         'keytool'])
            else:
                db.plugin_phantermobileconstructor_keystore.keytool.default = keytool[
                    'keytool'][0]
        form = SQLFORM(db.plugin_phantermobileconstructor_keystore)
    else:
        q_keystore = db(
            db.plugin_phantermobileconstructor_keystore).select().first()
        form = SQLFORM(
            db.plugin_phantermobileconstructor_keystore, q_keystore.id)

    if form.process().accepted:
        session.flash = "Keystore configured!"
        redirect(URL('plugin_phantermobileconstructor', 'index'))

    return dict(form=form)

def echo_comand():
    try: 
        import simplejson as json
    except ImportError:
        import json
    
    if request.args(0) == 'buildhtml':
        phanterandroid.buildHtml()
        return '$("#status_compilar").html(%s)' % json.dumps(SPAN("Compiled", _style="color:#165016").xml().decode('utf-8'))
    elif request.args(0) == 'info':
        if request.vars.phonegapstatus:
            status = phanterandroid.statusServer()
            print("stataus phonegap",status)
            jquery = ""
            if status:
                html_status = SPAN(T("Running on port "), SPAN(
                    status['port']), _style="color:#165016")
            else:
                if request.vars.tryagain:
                    html_status = SPAN(
                        "Stoped! Get status again in 5 secondes", _style="color:#165016")
                    new_ajax = URL(args=request.args, vars=request.vars)
                    jquery = "setTimeout(function(){ajax('%s',[],':eval'); console.log('3 segundos');}, 5000);" % new_ajax
                else:
                    html_status = SPAN("Stoped", _style="color:#165016")
            return '$("#status_servidor_phonegap").html(%s); %s' % (json.dumps(html_status.xml().decode('utf-8')), jquery)
        elif request.vars.cordovastatus:
            status = phanterandroid.statusServer('cordova')
            jquery = ""
            print("status cordova",status)
            if status:
                html_status = SPAN(T("Running on port: "), SPAN(
                    status['port']), _style="color:#165016")
            else:
                if request.vars.tryagain:
                    html_status = SPAN(
                        "Stoped! Get status again in 5 secondes", _style="color:#165016")
                    new_ajax = URL(args=request.args, vars=request.vars)
                    jquery = "setTimeout(function(){ajax('%s',[],':eval'); console.log('3 segundos');}, 5000);" % new_ajax
                else:
                    html_status = SPAN("Stoped", _style="color:#165016")
            return '$("#status_servidor_cordova").html(%s); %s' % (json.dumps(html_status.xml().decode('utf-8')), jquery)
    elif request.args(0) == 'closeserver':
        phanterandroid.closeServer()
        return "alert('Server Closed!');"

    elif request.args(0) == 'resetapp':
        phanterandroid.resetApp()
        return "alert('Reset Done!');"
    elif request.args(0) == 'createapk':
        signed = False
        apk_file = None
        levelfile = 'debug'
        if db(db.plugin_phantermobileconstructor_apps).isempty() and db(db.plugin_phantermobileconstructor_keystore).isempty():
            return "$('#dowload_newapk_release').html('<span>First config xml and create keystore</span>'); $('#dowload_newapk_debug').html('<span>First config xml</span>')"
        elif db(db.plugin_phantermobileconstructor_apps).isempty():
            return "$('#dowload_newapk_release').html('<span>First config xml</span>'); $('#dowload_newapk_debug').html('<span>First config xml</span>')"

        q_apps_config = db(
            db.plugin_phantermobileconstructor_apps).select().first()
        q_keystore = db(
            db.plugin_phantermobileconstructor_keystore).select().first()
        if not request.vars.getlastapk:
            if request.args(1) == 'release':
                if q_keystore:
                    key_created = phanterandroid.createKeystore(
                        keytool=os.path.join(q_keystore.keytool),
                        keyname=q_keystore.keyname,
                        aliasname=q_keystore.aliasname,
                        validity=q_keystore.validity,
                        storepass=q_keystore.storepass,
                        keypass=q_keystore.keypass,
                        CN=q_keystore.common_name,
                        OU=q_keystore.organization_unit,
                        O=q_keystore.organization,
                        L=q_keystore.district,
                        ST=q_keystore.yourstate,
                        C=q_keystore.country
                    )
                    if key_created:
                        my_file = open(key_created[0], 'rb')
                        q_keystore.update_record(appkeystore=db.plugin_phantermobileconstructor_keystore.appkeystore.store(
                            my_file, "%s.keystore" % q_keystore.keyname))
                        db.commit()
                        signed = True

                phanterandroid.createApk('release')
                levelfile = 'release'
            else:
                phanterandroid.createApk()
                levelfile = 'debug'
        else:
            if q_keystore:
                if q_keystore.appkeystore and request.args(1) == 'release':
                    levelfile = 'release'
                    signed = True
            if request.args(1) == 'release':
                levelfile = 'release'
            else:
                levelfile = 'debug'

        basedirapk = os.path.join(request.env.web2py_path, 'cordova',
                                  request.application, 'platforms', 'android', 'build', 'outputs', 'apk')
        if levelfile == 'debug':
            if os.path.exists(os.path.join(basedirapk, 'android-debug.apk')):
                apk_file = os.path.join(basedirapk, 'android-debug.apk')

        else:
            if signed:
                if os.path.exists(os.path.join(basedirapk, 'android-release.apk')):
                    apk_file = os.path.join(basedirapk, 'android-release.apk')
            else:
                if os.path.exists(os.path.join(basedirapk, 'android-release-unsigned.apk')):
                    apk_file = os.path.join(
                        basedirapk, 'android-release-unsigned.apk')

        if apk_file:
            q_apk = db(
                (db.plugin_phantermobileconstructor_apks.application == q_apps_config.id) &
                (db.plugin_phantermobileconstructor_apks.apklevel == levelfile) &
                (db.plugin_phantermobileconstructor_apks.signed == signed)
            ).select().first()

            if signed and levelfile == 'release':
                apk_saved_name = "%s-release.apk" % q_apps_config.appname
            elif levelfile == 'release':
                apk_saved_name = "%s-release-unsigned.apk" % q_apps_config.appname
            else:
                apk_saved_name = "%s-debug.apk" % q_apps_config.appname
            if request.vars.getlastapk and q_apk.apkfile:
                downloadapk = q_apk.apkfile
                if request.args(1) == 'release':
                    return "$('#dowload_newapk_release').html(%s)" % (json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_release'), _href=URL('default', 'download', args=[downloadapk]))).xml().decode('utf-8')))
                else:
                    return "$('#dowload_newapk_debug').html(%s)" % (json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_release'), _href=URL('default', 'download', args=[downloadapk]))).xml().decode('utf-8')))
            else:
                if q_apk:
                    id_apk = q_apk.id
                    db.plugin_phantermobileconstructor_apks[q_apk.id] = {
                        'apkfile': db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), apk_saved_name),
                        'signed': signed
                    }
                else:
                    id_apk = db.plugin_phantermobileconstructor_apks.insert(**{
                        'apkfile': db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), apk_saved_name),
                        'apklevel': levelfile,
                        'signed': signed
                    })
            downloadapk = db.plugin_phantermobileconstructor_apks[
                id_apk].apkfile
            db.commit()
            if request.args(1) == 'release':
                return "$('#dowload_newapk_release').html(%s)" % (json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_release'), _href=URL('default', 'download', args=[downloadapk]))).xml().decode('utf-8')))
            else:
                return "$('#dowload_newapk_debug').html(%s)" % (json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_debug'), _href=URL('default', 'download', args=[downloadapk]))).xml().decode('utf-8')))
        else:
            if request.args(1) == 'release':
                return "$('#dowload_newapk_release').html(%s);" % (json.dumps("<span>Apk don't created!</span>"))
            else:
                return "$('#dowload_newapk_debug').html(%s);" % (json.dumps("<span>Apk don't created!</span>"))

    else:
        return "console.log('Notingh to do!');"

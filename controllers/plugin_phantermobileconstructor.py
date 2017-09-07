# -*- coding: utf-8 -*-
import os
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
    raise HTTP(200, T('PhanterMobile Constructor só funciona localmente'))
precisa_autorizacao = ['index', 'echo_comand']

if (request.function in precisa_autorizacao):
    if not gluon.fileutils.check_credentials(request):
        redirect(URL('admin', 'default', 'index',
                     vars=dict(send=URL(args=request.args, vars=request.vars))))

def index():
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    q_config=None
    if db(db.plugin_phantermobileconstructor_apps).isempty():
        appname, version, idapp = request.application, '0.0.1', 'com.yoursite.youapp'
    else:
        q_config=db(db.plugin_phantermobileconstructor_apps).select().first()
        appname, version, idapp = q_config.appname, q_config.apkversion, q_config.idapp

    
    if request.args(0)=='phonegap':
        android = PhanterAndroid()
        android.openServer()
        html = DIV(
                    DIV(
                        DIV(
                            DIV(
                                IFRAME(_src="http://%s:%s/" %(http_host, android.port), _class='iframe_mobile_portrait responsivo'),
                                _class='html_mobile_portrait responsivo'),
                            _class="mobile_portrait responsivo"),
                        _class="painel_esquerdo_g"),
                    DIV(DIV(H1(T('View in PhoneGap Server')), _class='caixa_titulo_painel_direito_g'),
                        DIV(
                            DIV(
                                IFRAME(_src="http://%s:%s/" %(http_host, android.port), _class='iframe_mobile_landscape responsivo'),
                                _class='html_mobile_landscape responsivo'),
                            _class="mobile_landscape responsivo"),
                        _class="painel_direito_g"),
                    _class="painel_principal_g caixa_view_semdistracoes_landscape")
    elif request.args(0)=='cordova':
        android = PhanterAndroid()
        android.openServer('cordova') 
        html = DIV(
                    DIV(
                        DIV(
                            DIV(
                                IFRAME(_src="http://%s:%s/browser/www" %(http_host, android.port), _class='iframe_mobile_portrait responsivo'),
                                _class='html_mobile_portrait responsivo'),
                            _class="mobile_portrait responsivo"),
                        _class="painel_esquerdo_g"),
                    DIV(DIV(H1(T('View in Cordova Server')), _class='caixa_titulo_painel_direito_g'),
                        DIV(
                            DIV(
                                IFRAME(_src="http://%s:%s/browser/www" %(http_host, android.port), _class='iframe_mobile_landscape responsivo'),
                                _class='html_mobile_landscape responsivo'),
                            _class="mobile_landscape responsivo"),
                        _class="painel_direito_g"),
                    _class="painel_principal_g caixa_view_semdistracoes_landscape")
    elif request.args(0)=='localview':
        html = DIV(
                    DIV(
                        DIV(
                            DIV(
                                IFRAME(_src="http://%s/%s/plugin_phantermobileconstructor/www_index" %(request.env.http_host, request.application), _class='iframe_mobile_portrait responsivo'),
                                _class='html_mobile_portrait responsivo'),
                            _class="mobile_portrait responsivo"),
                        _class="painel_esquerdo_g"),
                    DIV(DIV(H1(T('View in Web2py Server')), _class='caixa_titulo_painel_direito_g'),
                        DIV(
                            DIV(
                                IFRAME(_src="http://%s/%s/plugin_phantermobileconstructor/www_index" %(request.env.http_host, request.application), _class='iframe_mobile_landscape responsivo'),
                                _class='html_mobile_landscape responsivo'),
                            _class="mobile_landscape responsivo"),
                        _class="painel_direito_g"),
                    _class="painel_principal_g caixa_view_semdistracoes_landscape")
    else:
        if q_config:
            html_apks=DIV(DIV(H4('APK List')),_style='width:100%; display:table;text-align:center;')
            for x in db(db.plugin_phantermobileconstructor_apks.application==q_config.id).select():
                html_apks.append(DIV(A(_href=URL('default', 'download', args=[x.apkfile])), _style='float:left; margin:5px; padding:5px; baranground-color:grey;'))
        html = DIV(
        DIV(
            DIV(
                DIV(
                    IFRAME(
                        _src="http://%s/%s/plugin_phantermobileconstructor/www_index" %(request.env.http_host, request.application), 
                        _class='iframe_mobile_portrait responsivo'),
                    _class='html_mobile_portrait responsivo'), 
                _class="mobile_portrait responsivo"),
            _class='painel_esquerdo_g'),
        DIV(
            DIV(H1('PhanterMobile Constructor'), _class='caixa_titulo_painel_direito_g'),
            DIV(DIV(H3(STRONG('App Name: ', _style='color:orange'), appname, STRONG(' Version: ', _style='color:orange'), version, STRONG(' ID: ', _style='color:orange'), idapp), _style="text-align:center;"),
                DIV(
                    DIV(
                        DIV(T("Compile html"), _class="center_table_cell"), 
                        _alvo="#status_compilar",
                        _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['buildhtml']),
                        _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                    DIV(_id="status_compilar", _class='status_botao_principal'), 
                    _class="caixa_botao_ajax_principal",
                    ),
                DIV(
                    A(
                        DIV(T("Open phonegap server"), _class="center_table_cell"),
                        _alvo="#status_servidor_phonegap",
                        _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['info'], vars={'phonegapstatus':True, 'tryagain':True}),
                        _href=URL(args=['phonegap']),
                        _target="_blank",
                        _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                    DIV(SPAN("Without Status", _style='color:grey;'), _id='status_servidor_phonegap',_class='status_botao_principal'), 
                    _class="caixa_botao_ajax_principal",
                    ),
                DIV(
                    A(
                        DIV(T("Open cordova server"), _class="center_table_cell"), 
                        _alvo="#status_servidor_cordova",
                        _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['info'], vars={'cordovastatus':True, 'tryagain':True}),
                        _href=URL(args=['cordova']),
                        _target="_blank",
                        _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                    DIV(SPAN("Without Status", _style='color:grey;'), _id='status_servidor_cordova',_class='status_botao_principal'),
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
                        _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['createapk', 'debug']),
                        _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                    DIV(_id="dowload_newapk_debug", _class='status_botao_principal'), 
                    _class="caixa_botao_ajax_principal",
                    ),
                DIV(
                    DIV(DIV(T("Create Release APK"), _class="center_table_cell"), 
                        _alvo="#dowload_newapk_release",
                        _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['createapk', 'release']),
                        _class='phantermobile-botao-ajax botao_pagina_principal_comandos'),
                    DIV(_id="dowload_newapk_release", _class='status_botao_principal'), 
                    _class="caixa_botao_ajax_principal",
                    ),
                DIV(
                    A(
                        DIV(T("Config XML"), _class="center_table_cell"), 
                        _alvo="#status_config_xml",
                        _href=URL('configxml'),
                        _class='botao_pagina_principal_comandos'),
                    DIV(SPAN("Create first Config.xml", _style='color:red;') if db(db.plugin_phantermobileconstructor_apps).isempty() else "", _id='status_config_xml',_class='status_botao_principal'),
                    _class="caixa_botao_ajax_principal",
                    ),
                DIV(
                    A(
                        DIV(T("Config KeyStore"), _class="center_table_cell"), 
                        _alvo="#status_config_keystore",
                        _href=URL('configkeystore'),
                        _class='botao_pagina_principal_comandos'),
                    DIV(SPAN("Config your keystore", _style='color:red;') if db(db.plugin_phantermobileconstructor_keystore).isempty() else "", _id='status_config_keystore',_class='status_botao_principal'),
                    _class="caixa_botao_ajax_principal",
                    ),
                _class='caixa_comandos'),
            _class='painel_direito_g'),
        _class='painel_principal_g')
    return locals()

def configxml():
    response.flash=T("Edit config.xml of app")
    q_config=db(db.plugin_phantermobileconstructor_apps).select().first()
    form=SQLFORM(db.plugin_phantermobileconstructor_apps, q_config.id if q_config else None, showid=False)
    if form.process().accepted: 
        if not os.path.exists(os.path.join(request.env.web2py_path, 'cordova', request.application,'config.xml')):
            from phanterandroid import PhanterAndroid
            android=PhanterAndroid()
        meuxml=parseConfigXML(os.path.join(request.env.web2py_path, 'cordova', request.application,'config.xml'))
        meuxml.appname=form.vars.appname
        meuxml.description=form.vars.description
        meuxml.authorname=form.vars.authorname
        meuxml.apkversion=form.vars.apkversion
        meuxml.idapp=form.vars.idapp
        meuxml.authoremail=form.vars.authoremail
        meuxml.authorwebsite=form.vars.authorwebsite
        for x in form.vars.externalacess:
            meuxml.addElementList('access', 'origin', x)
        for y in form.vars.allownavigation:
            meuxml.addElementList('allow-navigation', 'origin', y)
        for z in form.vars.allowintent:
            meuxml.addElementList('allow-intent', 'origin', z)
            
        meuxml.write(os.path.join(r'C:\web2py_mobiletest\cordova\welcome\config2.xml'))
        session.flash="config.xml saved!"
        print session.flash
        redirect(URL('plugin_phantermobileconstructor','index'))
    if form.errors:
        response.flash=T("Problems in form!")
    return dict(form=form)

def configkeystore():
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android = PhanterAndroid()  
    if db(db.plugin_phantermobileconstructor_keystore).isempty():
        db.plugin_phantermobileconstructor_keystore.appkeystore.readable=False
        db.plugin_phantermobileconstructor_keystore.appkeystore.writable=False
        keytool=android.requeriments('keytool')

        print keytool
        if keytool['keytool']:
            if len(keytool['keytool']) > 1:
                db.plugin_phantermobileconstructor_keystore.keytool.default=keytool['keytool'][0]
                db.plugin_phantermobileconstructor_keystore.keytool.requires=IS_IN_SET(keytool['keytool'])
            else:
                db.plugin_phantermobileconstructor_keystore.keytool.default=keytool['keytool'][0]
        form=SQLFORM(db.plugin_phantermobileconstructor_keystore)
    else:
        q_keystore=db(db.plugin_phantermobileconstructor_keystore).select().first()
        form=SQLFORM(db.plugin_phantermobileconstructor_keystore, q_keystore.id)

    if form.process().accepted:
        session.flash="Keystore configured!"
        redirect(URL('plugin_phantermobileconstructor','index'))
    
    return dict(form=form)

def echo_comand():

    import json
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android = PhanterAndroid()

    if request.args(0) == 'buildhtml':
        android.buildHtml()
        return '$("#status_compilar").html(%s)' %json.dumps(SPAN("Compiled", _style="color:#165016").xml())
    elif request.args(0)=='info':
        if request.vars.phonegapstatus:
            status=android.statusServer()
            jquery=""
            if status:
                html_status=SPAN(T("Running on port "), SPAN(status['port']), _style="color:#165016")
            else:
                if request.vars.tryagain:
                    html_status=SPAN("Stoped! Get status again in 5 secondes", _style="color:#165016")
                    new_ajax=URL(args=request.args, vars=request.vars)
                    jquery="setTimeout(function(){ajax('%s',[],':eval'); console.log('3 segundos');}, 5000);" %new_ajax
                else:
                    html_status=SPAN("Stoped", _style="color:#165016")
            return '$("#status_servidor_phonegap").html(%s); %s' %(json.dumps(html_status.xml()),jquery)
        elif request.vars.cordovastatus:
            status=android.statusServer('cordova')
            jquery=""
            if status:
                html_status=SPAN(T("Running on port: "), SPAN(status['port']), _style="color:#165016")
            else:
                if request.vars.tryagain:
                    html_status=SPAN("Stoped! Get status again in 5 secondes", _style="color:#165016")
                    new_ajax=URL(args=request.args, vars=request.vars)
                    jquery="setTimeout(function(){ajax('%s',[],':eval'); console.log('3 segundos');}, 5000);" %new_ajax
                else:
                    html_status=SPAN("Stoped", _style="color:#165016")
            return '$("#status_servidor_cordova").html(%s); %s' %(json.dumps(html_status.xml()),jquery)
    elif request.args(0) == 'closeserver':
        android.closeServer()
        return "alert('Server Closed!');"

    elif request.args(0) == 'resetapp':
        android.resetApp()
        return "alert('Reset Done!');"
    elif request.args(0)== 'createapk':
        signed=False
        apk_file=None
        levelfile='debug'
        if db(db.plugin_phantermobileconstructor_apps).isempty() and db(db.plugin_phantermobileconstructor_keystore).isempty():
            return "$('#dowload_newapk_release').html('<span>First config xml and create keystore</span>'); $('#dowload_newapk_debug').html('<span>First config xml</span>')"
        elif db(db.plugin_phantermobileconstructor_apps).isempty():
            return "$('#dowload_newapk_release').html('<span>First config xml</span>'); $('#dowload_newapk_debug').html('<span>First config xml</span>')"

        q_apps_config=db(db.plugin_phantermobileconstructor_apps).select().first()
        q_keystore=db(db.plugin_phantermobileconstructor_keystore).select().first()
        if not request.vars.getlastapk:
            if request.args(1)=='release':
                if q_keystore:
                    key_created=android.createKeystore(
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
                        print key_created[0]
                        my_file=open(key_created[0], 'rb')
                        q_keystore.update_record(appkeystore=db.plugin_phantermobileconstructor_keystore.appkeystore.store(my_file, "%s.keystore" %q_keystore.keyname))
                        db.commit()                      
                        signed=True

                android.createApk('release')
                levelfile='release'
            else:
                android.createApk()
                levelfile='debug'
        else:
            if q_keystore:
                if q_keystore.appkeystore and request.args(1)=='release':
                    levelfile='release'
                    signed=True
            if request.args(1)=='release':
                    levelfile='release'               
            else:

                levelfile='debug'

       
        basedirapk=os.path.join(request.env.web2py_path,'cordova', request.application, 'platforms', 'android', 'build', 'outputs', 'apk')
        if levelfile=='debug':
            if os.path.exists(os.path.join(basedirapk, 'android-debug.apk')):
                apk_file=os.path.join(basedirapk, 'android-debug.apk')

        else:
            if signed:
                if os.path.exists(os.path.join(basedirapk, 'android-release.apk')):
                    apk_file=os.path.join(basedirapk, 'android-release.apk')
            else:
                if os.path.exists(os.path.join(basedirapk, 'android-release-unsigned.apk')):
                    apk_file=os.path.join(basedirapk, 'android-release-unsigned.apk')

        if apk_file:
            q_apk=db(
                (db.plugin_phantermobileconstructor_apks.application==q_apps_config.id)&
                (db.plugin_phantermobileconstructor_apks.apklevel==levelfile)&
                (db.plugin_phantermobileconstructor_apks.signed==signed)
                ).select().first()

            if signed and levelfile=='release':
                apk_saved_name="%s-release.apk" %q_apps_config.appname
            elif levelfile=='release':
                apk_saved_name="%s-release-unsigned.apk" %q_apps_config.appname
            else:
                apk_saved_name="%s-debug.apk" %q_apps_config.appname
            if request.vars.getlastapk and q_apk.apkfile:
                downloadapk=q_apk.apkfile
                if request.args(1)=='release':
                    return "$('#dowload_newapk_release').html(%s)" %(json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_release'),_href=URL('default','download', args=[downloadapk]))).xml()))
                else:
                    return "$('#dowload_newapk_debug').html(%s)" %(json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_release'),_href=URL('default','download', args=[downloadapk]))).xml()))
            else:
                if q_apk:
                    id_apk=q_apk.id
                    db.plugin_phantermobileconstructor_apks[q_apk.id]={
                        'apkfile':db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), apk_saved_name),
                        'signed':signed
                        }
                else:
                    id_apk=db.plugin_phantermobileconstructor_apks.insert(**{
                        'apkfile':db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), apk_saved_name),
                        'apklevel':levelfile,
                        'signed':signed
                        })
            downloadapk=db.plugin_phantermobileconstructor_apks[id_apk].apkfile
            db.commit()
            if request.args(1)=='release':
                return "$('#dowload_newapk_release').html(%s)" %(json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_release'),_href=URL('default','download', args=[downloadapk]))).xml()))
            else:
                return "$('#dowload_newapk_debug').html(%s)" %(json.dumps(SPAN(A(DIV(apk_saved_name, _class='download_newapk_debug'),_href=URL('default','download', args=[downloadapk]))).xml()))
        else:
            return "$('#dowload_newapk_debug').html(%s); $('#dowload_newapk_release').html(%s);" %(json.dumps("<span>Apk don't created!</span>"), json.dumps("<span>Apk don't created!</span>"))
    else:
        return "console.log('Notingh to do!');"


####################################
# Mobile app Functions(Views and Css)
####################################

# The generated css will be placed in the head of "www_layout.html"
def css_head_layout_www():
    return dict()


# Functions started with "www" in your name will generate the htmls that will be placed in the www folder of cordova
# Example: the function "def www_index ()" will be generated in the www
# folder the index.html file.

def www_index():
    return dict()






#This is necessary to convert links generated from URL() function to local links from Cordova App.
if request.vars.phantermobilebuild:

    def filter(d):
        import re
        if isinstance(d, dict):
            html_filtrado = re.compile(
                '\n\s\s+\n').sub('\n', response.render(d))
        else:
            html_filtrado = re.compile(
                '\n\s\s+\n').sub('\n', response.render(d()))
        html_filtrado = html_filtrado.replace(
            "/%s/static/plugin_phantermobileconstructor/www/" % request.application, "")
        html_filtrado = html_filtrado.replace(
            "%s/static/plugin_phantermobileconstructor/www/" % request.application, "")
        html_filtrado = html_filtrado.replace(
            "/static/plugin_phantermobileconstructor/www/", "")
        html_filtrado = html_filtrado.replace(
            "static/plugin_phantermobileconstructor/www/", "")
        return html_filtrado
    response._caller = filter

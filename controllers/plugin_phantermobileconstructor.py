# -*- coding: utf-8 -*-
import os
import gluon.fileutils

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
    response.flash = T("Welcome")
    if request.args(0)=='phonegap':
        android = PhanterAndroid()
        android.openServer()
        html = DIV(DIV(IFRAME(_src="http://localhost:%s/" % android.port, _class='iframe_mobile responsivo'),
                   _class='html_mobile responsivo'), _class="mobile responsivo")
    elif request.args(0)=='cordova':
        android = PhanterAndroid()
        android.openServer('cordova') 
        html = DIV(DIV(IFRAME(_src="http://localhost:%s/" % android.port, _class='iframe_mobile responsivo'),
                   _class='html_mobile responsivo'), _class="mobile responsivo")     
    else:
        print "http://localhost:%s/%s/plugin_phantermobileconstructor/www_index" %(request.application, request.env.server_port)
        html = DIV(
        DIV(
            DIV(
                DIV(
                    IFRAME(
                        _src="http://localhost:%s/%s/plugin_phantermobileconstructor/www_index" %(request.env.server_port, request.application), 
                        _class='iframe_mobile responsivo'),
                       _class='html_mobile responsivo'), 
                _class="mobile responsivo"),
        _class='painel_esquerdo_g'),
        DIV(
            DIV(H1('PhanterMobile Constructor'), _class='caixa_titulo_painel_direito_g'),
            DIV(
                DIV(DIV(DIV(T("Compile html"), _class="center_table_cell"), _class='botao_pagina_principal_comandos'),
                               DIV(_id="status_compilar", _class='status_botao_principal'), 
                               _class="phantermobile-botao-ajax caixa_botao_ajax_principal",
                               _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['buildhtml'])),
                A(DIV(DIV(T("Open phonegap server"), _class="center_table_cell"), _class='botao_pagina_principal_comandos'),
                               DIV(SPAN("Without Status", _style='color:grey;'), _id='status_servidor_phonegap',_class='status_botao_principal'), 
                               _class="phantermobile-botao-ajax caixa_botao_ajax_principal",
                               _href=URL(args=['phonegap']),
                               _target="blank",
                               _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['info'], vars={'phonegapstatus':True})),
                A(DIV(DIV(T("Open cordova server"), _class="center_table_cell"), _class='botao_pagina_principal_comandos'),
                               DIV(SPAN("Without Status", _style='color:grey;'), _id='status_servidor_cordova',_class='status_botao_principal'),
                               _class="phantermobile-botao-ajax caixa_botao_ajax_principal",
                               _href=URL(args=['cordova']),
                               _target="blank",
                               _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['info'], vars={'cordovastatus':True})),
                DIV(DIV(DIV(T("Create APK"), _class="center_table_cell"), _class='botao_pagina_principal_comandos'),
                               DIV(_id="dowload_newapk", _class='status_botao_principal'), 
                               _class="phantermobile-botao-ajax caixa_botao_ajax_principal",
                               _url_ajax=URL('plugin_phantermobileconstructor', 'echo_comand', args=['createapk'])),
                _class='caixa_comandos'),
            _class='painel_direito_g'),
        _class='painel_principal_g')
    return locals()


def echo_comand():

    import json
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android = PhanterAndroid()

    if request.args(0) == 'buildhtml':
        android.buildHtml()
        return '$("#status_compilar").html(%s)' %json.dumps(SPAM("Compiled", _style="color:green").xml())
    elif request.args(0)=='info':
        if request.vars.phonegapstatus:
            status=android.statusServer()
            if status:
                html_status=SPAN(T("Running on port "), SPAN(status['port']), _style="color:green")
            else:
                html_status=SPAN("Stoped", _style="color:green")
            return '$("#status_servidor_phonegap").html(%s)' %json.dumps(html_status.xml())
        elif request.vars.cordovastatus:
            status=android.statusServer('cordova')
            if status:
                html_status=SPAN(T("Running on port: "), SPAN(status['port']), _style="color:green")
            else:
                html_status=SPAN("Stoped", _style="color:green")
            return '$("#status_servidor_cordova").html(%s)' %json.dumps(html_status.xml())
    elif request.args(0) == 'closeserver':
        android.closeServer()
        return "alert('Server Closed!');"

    elif request.args(0) == 'resetapp':
        android.resetApp()
        return "alert('Reset Done!');"
    elif request.args(0)== 'createapk':
        #android.createApk()        levelfile=''
        basedirapk=os.path.join(request.env.web2py_path,'cordova', request.application, 'platforms', 'android', 'build', 'outputs', 'apk')
        if os.path.exists(os.path.join(basedirapk, 'android-debug.apk')) or  os.path.exists(os.path.join(basedirapk, '%s-debug.apk' %request.application)):
            if os.path.exists(os.path.join(basedirapk, 'android-debug.apk')):
                apk_file=os.path.join(basedirapk, 'android-debug.apk')
                os.rename(apk_file, os.path.join(basedirapk, '%s-debug.apk' %request.application))
            apk_file=os.path.join(basedirapk, '%s-debug.apk' %request.application)
            levelfile="debug"
            if request.vars.version and request.vars.appname:
                q_apk=db((db.plugin_phantermobileconstructor_apks.versioapk==request.vars.version)&
                    (db.plugin_phantermobileconstructor_apks.appname==request.vars.appname)&
                    (db.plugin_phantermobileconstructor_apks.appname==levelfile)
                    ).select().first()

                if q_apk:
                    id_apk=q_apk.id
                    db.plugin_phantermobileconstructor_apks[q_apk.id]={
                        'apkfile':db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), '%s-debug.apk' %request.application)
                        }
                else:
                    id_apk=db.plugin_phantermobileconstructor_apks.insert(**{
                        'apkfile':db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), '%s-debug.apk' %request.application),
                        'appname': request.vars.appname,
                        'apkversion': request.vars.version,
                        'apklevel':levelfile,
                        })
            else:
                id_apk=db.plugin_phantermobileconstructor_apks.insert(**{
                    'apkfile':db.plugin_phantermobileconstructor_apks.apkfile.store(open(apk_file, 'rb'), '%s-debug.apk' %request.application),
                    'appname': request.aplication,
                    'apkversion': '1.0.0',
                    'apklevel':levelfile,
                    })
            downloadapk=db.plugin_phantermobileconstructor_apks[id_apk].apkfile
            db.commit()
            return "$('#dowload_newapk').html(%s)" %(json.dumps(SPAN(A(DIV('%s-debug.apk' %request.application, _class='download_newapk'),_href=URL('default','download', args=[downloadapk]))).xml()))


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

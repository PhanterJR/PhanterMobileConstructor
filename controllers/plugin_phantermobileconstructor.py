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
    else:
        print "http://localhost:%s/%s/plugin_phantermobileconstructor/www_index" %(request.application, request.env.server_port)
        html = DIV(DIV(IFRAME(_src="http://localhost:%s/%s/plugin_phantermobileconstructor/www_index" %(request.env.server_port, request.application), _class='iframe_mobile responsivo'),
                   _class='html_mobile responsivo'), _class="mobile responsivo")
    return locals()


def echo_comand():
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android = PhanterAndroid()

    if request.args(0) == 'buildhtml':
        android.buildHtml()
        return "lert('Html Compiled!');"

    elif request.args(0) == 'closeserver':
        android.closeServer()
        return "alert('Server Closed!');"

    elif request.args(0) == 'resetapp':
        android.resetApp()
        return "alert('Reset Done!');"

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

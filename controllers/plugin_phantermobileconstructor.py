# -*- coding: utf-8 -*-

import os
import gluon.contenttype
import gluon.fileutils
from gluon._compat import iteritems


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
precisa_autorizacao=['index', 'close', 'build']

# if (request.application == 'admin' and not session.authorized) or \
#         (request.application != 'admin' and not gluon.fileutils.check_credentials(request)):
#     redirect(URL('admin', 'default', 'index',
#                  vars=dict(send=URL(args=request.args, vars=request.vars))))
if (request.function in precisa_autorizacao):
    if not gluon.fileutils.check_credentials(request):
        redirect(URL('admin', 'default', 'index',
                     vars=dict(send=URL(args=request.args, vars=request.vars))))

def index():
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android=PhanterAndroid()
    android.iniciarServidor()
    response.flash="Bem vindo"
    html=DIV(DIV(IFRAME(_src="http://localhost:%s/" %android.porta, _class='iframe_mobile responsivo'), _class='html_mobile responsivo'), _class="mobile responsivo")
    return locals()

def close():
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android=PhanterAndroid()
    android.close()
    return "ok"

def build():
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    android=PhanterAndroid()
    android.pre_build('index')
    return "location.reload()"

####################################
#Funcões do dispoositivo mobile
####################################

# O css gerado será colocado no head do "www_layout.html"
def css_head_layout_www():
    return dict()

# Das funcões iniciadas com www em seu nome serão gerados os htmls que serão colocados na pasta www do cordova
# Exemplo: da função "def www_index()" será gerado na pasta www o arquivo index.html.
def www_index():
    return dict()

if request.vars.phantermobilebuild:

    def filter(d):
        import re
        if isinstance(d,dict):
            html_filtrado=re.compile('\n\s\s+\n').sub('\n',response.render(d))
        else:
            html_filtrado=re.compile('\n\s\s+\n').sub('\n',response.render(d()))
        html_filtrado=html_filtrado.replace("/%s/static/plugin_phantermobileconstructor/www/" %request.application, "")
        html_filtrado=html_filtrado.replace("%s/static/plugin_phantermobileconstructor/www/" %request.application, "")
        html_filtrado=html_filtrado.replace("/static/plugin_phantermobileconstructor/www/", "")
        html_filtrado=html_filtrado.replace("static/plugin_phantermobileconstructor/www/", "")
        return html_filtrado
    response._caller=filter
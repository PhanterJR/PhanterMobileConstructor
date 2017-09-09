# -*- coding: utf-8 -*-
# requires corsproxy
# npm install -g corsproxy

# python battery
from sys import platform
import re
import subprocess
import os
from gluon import current

# this import need install (battery dont incluided)
import psutil

class PhanterAjaxDevelopment(object):
    def __init__(self, cmd_status=True):
        """
            The corsproxy is used in local development, local ajax request are blocked by CORs rules.
            Corsproxy will the Server/Client comunication.

            Example:
                in models:
                    phanterajaxdevelopment=PhanterAjaxDevelopment('localhost:8000/welcome/echos_ajax')
                    response.server_ajax=phanterajaxdevelopment.urlAjaxServer()

                in view:
                    <script>
                        var url_ajax="{{response.server_ajax}}/yourarg0/yourarg1?var1=teste1&var2=teste2"
                        ajax(url_ajax, [], ':eval')
                    </script>
        """
        self.request=current.request
        self.cordova_app_folder = os.path.join(
            self.request.env.web2py_path, 'cordova')
        if platform == "win32" or platform == 'cygwin':
            nome = 'node.exe'
        elif platform =='linux' or platform =='linux2':
            nome = 'node'
        processo_localizado = {}
        localized=False
        for proc in psutil.process_iter():
            if proc.name() == nome:
                    strcmdline = proc.cmdline()
                    linha_de_comando=' '.join(strcmdline)
                    if 'corsproxy' in linha_de_comando:
                        processo_localizado['server'] = 'corsproxy'
                        processo_localizado['port'] = 1337
                        processo_localizado['pid'] = proc.pid
                        if cmd_status:
                            print "\n================ SERVER PROXY ==================" +\
                                "\n Server: Corsproxy\n Porta: %s\n PID: %s\n" %(1337, proc.pid) +\
                                "------------------------------------\n"
        if not processo_localizado:
            if platform == 'win32' or platform == 'cygwin':
                re_corsproxy=re.compile(r'^[A-Z]:\\.+corsproxy\.cmd')
                path_corsproxy=None
                try:
                    corsproxy=subprocess.check_output(['where','corsproxy.cmd'])
                    corsproxy=corsproxy.strip().split('\n')[0]
                    path_corsproxy=re_corsproxy.findall(corsproxy)
                except Exception as e:
                    print "Don't find corsproxy in your system, try install. eg. npm install -g corsproxy"
                    print e
                if path_corsproxy:
                    with open(os.path.join(self.cordova_app_folder, 'server_run_corsproxy.bat'), 'w') as file_opened:
                        file_opened.write("corsproxy")
                    processo = subprocess.Popen([os.path.join(
                    self.cordova_app_folder, 'server_run_corsproxy.bat')], shell=True)          
                    print "\n================ SERVER PROXY ==================" +\
                        "\n Server: Corsproxy\n Porta: %s\n PID: %s\n" %(1337, processo.pid) +\
                        "------------------------------------\n"
            elif platform == 'linux' or platform == 'linux2':
                if server_chosen=='cordova':
                    subprocess.call(['cordova prepare'], shell=True, cwd=self.aplication_folder)
                processo = subprocess.Popen(['%S serve %s' %(self.server_chosen, port)], shell=True, cwd=self.aplication_folder)                


    def urlAjaxServer(self, url_ajax):
        """
        @url_ajax: target server. eg. localhost:8000/controller (default web2py host)
        """
        url="http://localhost:1337/%s/" %url_ajax
        return url


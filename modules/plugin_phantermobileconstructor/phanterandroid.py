# -*- coding: utf-8 -*-
# versao: 1.2.0
import subprocess
import os
import zipfile
import psutil
import urllib2
import shutil
import time
import re
from gluon.html import URL
from gluon import current
from gluon.compileapp import find_exposed_functions


class PhanterAndroid(object):
    """Make the connection between cordova app and web2py app

        - On init create this folders structure if not exists:
           web2py
            | - cordova
                    |-folderAppCordova

        - The name of folderAppCordova is the same of your web2py aplication
            Cointains the default cordova app

        - On Web2py Developer, inside of plugin_phantermobileconstructor, 
            all functions started with "www_" will be rendered in the cordova application (on buildHtml method)
            and all files in static/plugin_phantermobileconstructor/www will be copied to the www folder of cordova App

            exemple:
                - On controller plugin_phantermobileconstructor.py
                    def www_index():
                        #your code
                        return dict()
                    def www_other_function():
                        return DIV("my div")

                - On static/plugin_phantermobileconstructor/www
                    static/plugin_phantermobileconstructor/www/
                            |-css/
                                |-mycss.css
                                |-outhes.css
                            |-images/
                                |-myimage.jpg
                            |-js/
                                |-Jquery.js

                - will generate the following structure in the cordova application:
                    folderAppCordova/
                        |-www/
                            |-index.html
                            |-outher_function.html
                            |-css/
                                |-mycss.css
                                |-outhes.css
                            |-images/
                                |-myimage.jpg
                            |-js/
                                |-Jquery.js
    """

    def __init__(self, application_id=None):
        """@aplication_id: generally follows the following format: com.yoursite.youraplication
              eg. br.com.conexaodidata.myaplication
        """
        self.request = current.request
        self.aplication_name = self.request.application
        if not application_id:
            self.aplication_id = "com.yoursite.www"
        else:
            self.aplication_id = application_id
        self.ports = []
        self.port = 3000
        self.cordova_app_folder = os.path.join(
            self.request.env.web2py_path, 'cordova')
        self.aplication_folder = os.path.join(
            self.cordova_app_folder, self.aplication_name)
        self.server_chosen = 'phonegap'

        tem_condova = os.path.exists(self.cordova_app_folder)
        tem_aplicativo = os.path.exists(self.aplication_folder)
        if not tem_condova or not tem_aplicativo:
            self._prepareTheEnvironment(buildHtml=True)

    def openServer(self, server='phonegap'):
        """
            @server: 'phonegap' or 'cordova'
            In linux the server will have to be opened manually, 
            so the method will try to find the process and the port.
        """
        request = self.request
        if server != self.server_chosen:
            self.server_chosen = server
        print "Open %s server..." % self.server_chosen
        procs = self._examine_process()
        if procs:
            self.port = procs['port']
            print 'Server is run in door %s' % procs['port']
        else:
            port = 3000
            for y in xrange(3000, 4000):
                if y in self.ports:
                    pass
                else:
                    self.ports.append(y)
                    port = y
                    break
            self.port = port
            if self.server_chosen == 'phonegap':
                with open(os.path.join(self.cordova_app_folder, 'server_run_%s.bat' % self.aplication_name), 'w') as arquivo_aberto:
                    conteudo = "cd %s\nphonegap serve -p%s" % (
                        self.aplication_folder, port)
                    arquivo_aberto.write(conteudo)
            else:
                with open(os.path.join(self.cordova_app_folder, 'server_run_%s.bat' % self.aplication_name), 'w') as arquivo_aberto:
                    conteudo = "cd %s\ncordova serve %s" % (
                        self.aplication_folder, port)
                    arquivo_aberto.write(conteudo)

            processo = subprocess.Popen([os.path.join(
                self.cordova_app_folder, 'server_run_%s.bat' % self.aplication_name)], shell=False)
            proc = psutil.Process(processo.pid)
            print "%s run on door %s" % (self.server_chosen, port)
            while True:
                print "Try conect (open url) to %s..." % ('http://localhost:%s' % port),
                if proc.children():
                    try:
                        urllib2.urlopen('http://localhost:%s' % port)
                        break
                    except Exception as e:
                        print "Fail! be patient! Waint 3 seconds..."
                        time.sleep(3)
                else:
                    time.sleep(1)
            print "\n================================\n  Conected\n-------------------------------\n"

    def closeServer(self):
        """
            Will try to find the server process and will close it
        """
        print "Closing..."
        procs = self._examine_process()
        if procs:
            proc = psutil.Process(procs['pid'])
            proc.kill()
        else:
            print 'Server not found. nothing to do'

    def buildHtml(self):
        """
            All functions started with "www_" will be rendered in the cordova application (on buildHtml method)
            and all files in static/plugin_phantermobileconstructor/www will be copied to the www folder of cordova App
        """
        request = self.request

        print "Compiling html..."
        self.close()

        origem = os.path.join(request.env.web2py_path, 'applications',
                              self.aplication_name, 'static', 'plugin_phantermobileconstructor', 'www')
        self.lista_de_pastas_origem_e_destino = []
        self.lista_de_pastas_destino = []
        self.lista_de_arquivos_origem_e_destinos = []
        self._examine_folders(origem)
        for y in self.lista_de_pastas_destino:
            if not os.path.exists(y):
                os.makedirs(y)
        for x in self.lista_de_arquivos_origem_e_destinos:
            shutil.copy(x[0], x[1])
        arquivo_plugin = os.path.join(request.env.web2py_path, 'applications',
                                      self.aplication_name, 'controllers', 'plugin_phantermobileconstructor.py')
        funcoes = []
        with open(arquivo_plugin, 'r') as arquivo_aberto:
            funcoes = find_exposed_functions(arquivo_aberto.read())
        if funcoes:
            for x in (x for x in funcoes if x.startswith("www_")):
                url = "%s?phantermobilebuild=True" % URL(
                    c='plugin_phantermobileconstructor', f=x, host=True)
                print "Try open url: %s" % url
                cont = 0
                nome_arquivo_html = x.replace('www_', '')
                while cont < 5:
                    try:
                        html_url = urllib2.urlopen(url)
                        html = html2 = html_url.read()
                        arquivo_destino = os.path.join(
                            self.aplication_folder, 'www', "%s.html" % nome_arquivo_html)
                        with open(arquivo_destino, 'w') as arquivo_aberto:
                            print 'Get html source of %s and copy to %s' % (url, arquivo_destino)
                            arquivo_aberto.write(html)
                        break
                    except Exception as e:
                        time.sleep(2)
                        print e
                        cont += 1
                        print "Fail! try %s of 5" % cont

    def _getServerandDoorCmdLine(self, cmdline):
        if 'serve' in cmdline:
            if 'phonegap' in cmdline:
                if '-p' in cmdline:
                    port = cmdline.split('-p')[-1].strip()
                    try:
                        port = int(port)
                    except:
                        print "error: port dont find!"
                        port = None
                    if port:
                        return ['phonegap', port]
                    else:
                        return []
                else:
                    return []
            elif 'cordova' in cmdline:
                padrao = re.compile('serve *([0-9]+)')
                port = padrao.findall(cmdline)
                try:
                    port = int(port)
                except:
                    print "error: port dont find!"
                    port = None
                if port:
                    return ['cordova', port]
                else:
                    return []
        else:
            return []

    def _examine_process(self):
        request = self.request
        print 'locating all server program process (Node.exe)...'
        nome = 'node.exe'
        processo_localizado = {}
        for proc in psutil.process_iter():
            if proc.name() == nome:
                if proc.cwd() == self.aplication_folder:
                    linha_de_comando = proc.cmdline()[-1]
                    port_and_server = self._getServerandDoorCmdLine(
                        linha_de_comando)
                    if port_and_server:
                        processo_localizado['server'] = port_and_server[0]
                        processo_localizado['port'] = port_and_server[1]
                        processo_localizado['pid'] = proc.pid
                        print "\n================ SERVER INFO ==================" +\
                            "\n Server: %s\n Porta: %s\n Pasta:%s \n PID: %s\n" % (port_and_server[0], port_and_server[1], proc.cwd(), proc.pid) +\
                            "------------------------------------\n"
        return processo_localizado

    def _examine_folders(self, path):
        request = self.request

        print "Examine folders..."
        if not os.path.isfile(path):
            lista = os.listdir(path)
            if lista:
                for x in lista:
                    if not os.path.isfile(os.path.join(path, x)):
                        self.lista_de_pastas_destino.append(os.path.join(path.replace(os.path.join(
                            request.env.web2py_path, 'applications', self.aplication_name, 'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.aplication_folder, 'www')), x))
                        self.lista_de_pastas_origem_e_destino.append([os.path.join(path, x),
                                                                      os.path.join(path.replace(os.path.join(request.env.web2py_path, 'applications', self.aplication_name,
                                                                                                             'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.aplication_folder, 'www')), x),
                                                                      ])
                        self._examine_folders(os.path.join(path, x))

                    else:
                        self.lista_de_arquivos_origem_e_destinos.append([os.path.join(path, x),
                                                                         os.path.join(path.replace(os.path.join(
                                                                             request.env.web2py_path, 'applications', self.aplication_name, 'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.aplication_folder, 'www'))),
                                                                         ])
        else:
            self.lista_de_arquivos_origem_e_destinos.append([os.path.join(path),
                                                             os.path.join(path.replace(os.path.join(request.env.web2py_path, 'applications', self.aplication_name,
                                                                                                    'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.aplication_folder, 'www'))),
                                                             ])

    def _prepareTheEnvironment(self, buildHtml=True):
        request = self.request

        print 'Prepare Environment'
        if not os.path.exists(self.cordova_app_folder):
            print 'Creating Folder: %s' % self.cordova_app_folder
            os.makedirs(self.cordova_app_folder)
        if not os.path.exists(os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name)):
            print "Creating file create_app_%s.bat" % self.aplication_name
            with open(os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name), 'w') as arquivo_aberto:
                conteudo = "cd %s\ncordova create %s %s %s" % (
                    self.cordova_app_folder, self.aplication_name, self.aplication_id, self.aplication_name)
                arquivo_aberto.write(conteudo)
        if not os.path.exists(self.aplication_folder):
            print "criando pasta do aplicativo: %s" % self.aplication_folder
            os.makedirs(self.aplication_folder)
            print "Executing: cordova create %s %s %s" % (self.aplication_name, self.aplication_name, self.aplication_name)
            subprocess.call([os.path.join(self.cordova_app_folder, 'create_app_%s.bat' %
                                          self.aplication_name)], stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE)
            print "copy template phanterandroid in: %s" % os.path.join(self.aplication_folder, 'www')
            print "unzip template of: %s" % os.path.abspath(os.path.join(os.path.dirname(__file__), 'phanterandroidpack', 'template.zip'))
            zip_ref = zipfile.ZipFile(os.path.abspath(os.path.join(
                os.path.dirname(__file__), 'phanterandroidpack', 'template.zip')), 'r')
            zip_ref.extractall(os.path.join(self.aplication_folder, 'www'))
            zip_ref.close()

        if buildHtml:
            self.buildHtml()
        else:


    def resetApp(self):
        self.removeCordovaApp()
        self.PrepareTheEnvironment(buildHtml=False)

    def removeCordovaApp(self):
        request = self.request

        self.close()
        print 'remove:', self.aplication_folder
        if os.path.exists(self.aplication_folder):
            try:
                shutil.rmtree(self.aplication_folder)
            except Exception as e:
                print "Erro on remove:", self.aplication_folder
                print e
        if os.path.exists(os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name)):
            try:
                os.unlink(os.path.join(self.cordova_app_folder,
                                       'create_app_%s.bat' % self.aplication_name))
            except Exception as e:
                print "Erro on remove:", os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name)
                print e
        if os.path.exists(os.path.join(self.cordova_app_folder, 'server_run_%s.bat' % self.aplication_name)):
            try:
                os.unlink(os.path.join(self.cordova_app_folder,
                                       'server_run_%s.bat' % self.aplication_name))
            except Exception as e:
                print "Erro on remove:", os.path.join(self.cordova_app_folder, 'server_run_%s.bat' % self.aplication_name)
                print e
if __name__ == "__main__":
    android = PhanterAndroid()
    android.openServer()

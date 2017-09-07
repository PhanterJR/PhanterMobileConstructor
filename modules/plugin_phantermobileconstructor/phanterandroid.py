# -*- coding: utf-8 -*-
# versao: 1.5.0

# python battery
import subprocess
import os
import zipfile
import urllib2
import shutil
import time
import re
from sys import platform

# this import need install (battery dont incluided)
import psutil

# imports from web2py
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
              NOTE: this option is obsolet
        """
        self.requeriments_store={
            'cordova':False,
            'keytool':False,
            'phonegap':False,
            'javac':False
        }
        self._created_key=[]
        self.request = current.request
        self.aplication_name = self.request.application
        if not application_id:
            self.aplication_id = "com.yoursite.yourapp"
        else:
            self.aplication_id = application_id
        self.ports = []
        self.port = 3000
        self.cordova_app_folder = os.path.join(
            self.request.env.web2py_path, 'cordova')
        self.aplication_folder = os.path.join(
            self.request.env.web2py_path, 'cordova', self.aplication_name)
        self.server_chosen = 'phonegap'
        self.requeriments_store
        tem_condova = os.path.exists(self.cordova_app_folder)
        tem_aplicativo = os.path.exists(self.aplication_folder)
        if not tem_condova or not tem_aplicativo:
            self._prepareTheEnvironment(buildHtml=True)

    def statusServer(self, server='phonegap', timewait=1):
        self.server_chosen = server
        time.sleep(timewait)
        return self._examine_process()

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
            if platform == "win32" or platform == 'cygwin':
                if self.server_chosen == 'phonegap':
                    with open(os.path.join(self.cordova_app_folder, 'server_%s_run_%s.bat' %(self.server_chosen, self.aplication_name)), 'w') as arquivo_aberto:
                        conteudo = "cd %s\nphonegap serve -p%s" % (
                            self.aplication_folder, port)
                        arquivo_aberto.write(conteudo)
                else:
                    with open(os.path.join(self.cordova_app_folder, 'server_%s_run_%s.bat' %(self.server_chosen, self.aplication_name)), 'w') as arquivo_aberto:
                        conteudo = "cd %s\ncordova prepare\ncordova serve %s" % (
                            self.aplication_folder, port)
                        arquivo_aberto.write(conteudo)

                processo = subprocess.Popen([os.path.join(
                    self.cordova_app_folder, 'server_%s_run_%s.bat' %(self.server_chosen, self.aplication_name))], shell=True)
            elif platform == "linux" or platform == "linux2":
                if server_chosen=='cordova':
                    subprocess.call(['cordova prepare'], shell=True, cwd=self.aplication_folder)
                processo = subprocess.Popen(['%S serve %s' %(self.server_chosen, port)], shell=True, cwd=self.aplication_folder)
            proc = psutil.Process(processo.pid)
            print "%s run on door %s" % (self.server_chosen, port)
            while True:
                print "Try conect (open url) to 'http://%s:%s'..." %(self.request.env.http_host.split(':')[0], port),
                if proc.children():
                    try:
                        urllib2.urlopen('http://%s:%s' %(self.request.env.http_host.split(':')[0], port))
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
        self.closeServer()

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
        strcmdline=' '.join(cmdline)
        if 'serve' in strcmdline:
            if 'phonegap' in strcmdline:
                if '-p' in strcmdline:
                    padrao = re.compile(r'serve *-[pP]([0-9]+)')
                    port = padrao.findall(strcmdline)
                    try:
                        port = int(port[0])
                    except:
                        print "error: port dont is a number!"
                        port = None
                    if port:
                        self.ports.append(port)
                        return ['phonegap', port]
                    else:
                        return []
                else:
                    return []
            elif 'cordova' in strcmdline:
                padrao = re.compile('serve *([0-9]+)')
                port = padrao.findall(strcmdline)
                try:
                    port = int(port[0])
                except:
                    print "error: port dont is a number!"
                    port = None
                if port:
                    self.ports.append(port)
                    return ['cordova', port]
                else:
                    return []
        else:
            return []

    def _examine_process(self):
        request = self.request
        print 'locating all server program process (Node.exe)...'
        if platform == "win32" or platform == 'cygwin':
            nome = 'node.exe'
        elif platform =='linux' or platform =='linux2':
            nome = 'node'
        processo_localizado = {}
        localized=False
        for proc in psutil.process_iter():
            if proc.name() == nome:
                if proc.cwd() == self.aplication_folder:
                    linha_de_comando = proc.cmdline()
                    port_and_server = self._getServerandDoorCmdLine(
                        linha_de_comando)
                    if port_and_server and not localized and (self.server_chosen==port_and_server[0]):
                        localized=True
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
        if platform == "win32" or platform == 'cygwin':

            if not os.path.exists(os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name)):
                print "Creating file create_app_%s.bat" % self.aplication_name
                with open(os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name), 'w') as arquivo_aberto:
                    conteudo = "cd %s\ncordova create %s %s %s\ncordova platform add browser" % (
                        self.cordova_app_folder, self.aplication_name, self.aplication_id, self.aplication_name)
                    arquivo_aberto.write(conteudo)
            if not os.path.exists(self.aplication_folder):
                print "Creating Folder cordova app: %s" % self.aplication_folder
                os.makedirs(self.aplication_folder)
                print "Executing: cordova create %s %s %s" % (self.aplication_name, self.aplication_id, self.aplication_name)
                subprocess.call([os.path.join(self.cordova_app_folder, 'create_app_%s.bat' %
                                              self.aplication_name)], stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE)
                print "copy template phanterandroid in: %s" % os.path.join(self.aplication_folder, 'www')
                print "unzip template of: %s" % os.path.abspath(os.path.join(os.path.dirname(__file__), 'phanterandroidpack', 'template.zip'))
                zip_ref = zipfile.ZipFile(os.path.abspath(os.path.join(
                    os.path.dirname(__file__), 'phanterandroidpack', 'template.zip')), 'r')
                zip_ref.extractall(os.path.join(self.aplication_folder, 'www'))
                zip_ref.close()
        elif platform == "linux" or platform == "linux2":
            if not os.path.exists(self.aplication_folder):
                subprocess.call(["cordova create %s %s %s" % (os.path.join(self.cordova_app_folder, self.aplication_name), self.aplication_id, self.aplication_name)], cwd=self.cordova_app_folder, shell=True)
                subprocess.call(["cordova platform add browser"], cwd=self.cordova_app_folder, shell=True)
                print "copy template phanterandroid in: %s" % os.path.join(self.aplication_folder, 'www')
                print "unzip template of: %s" % os.path.abspath(os.path.join(os.path.dirname(__file__), 'phanterandroidpack', 'template.zip'))
                zip_ref = zipfile.ZipFile(os.path.abspath(os.path.join(
                    os.path.dirname(__file__), 'phanterandroidpack', 'template.zip')), 'r')
                zip_ref.extractall(os.path.join(self.aplication_folder, 'www'))
                zip_ref.close()

        if buildHtml:
            self.buildHtml()

    def resetApp(self):
        self.removeCordovaApp()
        self.PrepareTheEnvironment(buildHtml=False)

    def _remove_file(self, file):
        if os.path.exists(file):
            try:
                os.unlink(file)
            except Exception as e:
                print "Erro on remove:", file
                print e

    def requeriments(self, update_req='all'):
        """try check requeriments
        @update: if all, all requirements will be checked.
            set 'cordova' to check cordova
            set 'keytool' to check keytool
            set 'phonegap' to check phonegap
            set 'javac' to check javac
        """
        if platform == 'win32' or platform == 'cygwin':
            re_cordova=re.compile(r'^[A-Z]:\\.+cordova\.cmd')
            re_phonegap=re.compile(r'^[A-Z]:\\.+phonegap\.cmd')
            re_keytool=re.compile(r'[A-Z]:\\.+\\Java\\.+bin\\keytool\.exe')
            re_javac=re.compile(r'[A-Z]:\\.+\\Java\\.+bin\\javac\.exe')
            if update_req=='all' or update_req=='cordova':
                try:
                    cordova=subprocess.check_output(['where','cordova.cmd'])
                    cordova=cordova.strip().split('\n')[0]
                    path_cordova=re_cordova.findall(cordova)
                    self.requeriments_store['cordova']=path_cordova
                except Exception as e:
                    print "Don't find cordova in your system, try install. eg. npm install -g cordova"
                    print e
            if update_req=='all' or update_req=='phonegap':
                try:
                    phonegap=subprocess.check_output(['where','phonegap.cmd'])
                    phonegap=phonegap.strip().split('\n')[0]
                    path_phonegap=re_phonegap.findall(phonegap)
                    self.requeriments_store['phonegap']=path_phonegap
                except Exception as e:
                    print "Don't find phonegap in your system, try install. eg. npm install -g phonegap"
                    print e
            if update_req=='all' or update_req=='keytool':
                try:
                    with open(os.path.join(self.cordova_app_folder, 'check_keytool.bat'), 'w') as arquivo_aberto:
                        arquivo_aberto.write('where /r "%ProgramW6432%\java" keytool.exe\nwhere /r "%ProgramFiles%\java" keytool.exe')
                    keytool=subprocess.Popen([os.path.join(self.cordova_app_folder, 'check_keytool.bat')], stdout=subprocess.PIPE)
                    result_keytool=keytool.stdout.read()
                    path_keytool=re_keytool.findall(result_keytool)
                    self.requeriments_store['keytool']=path_keytool
                except Exception as e:
                    print "Don't find keytool in your system, try install JAVA SDK"
                    print e  
            if update_req=='all' or update_req=='javac':
                try:
                    with open(os.path.join(self.cordova_app_folder, 'check_javac.bat'), 'w') as arquivo_aberto:
                        arquivo_aberto.write('where /r "%ProgramW6432%\java" javac.exe\nwhere /r "%ProgramFiles%\java" javac.exe')
                    javac=subprocess.Popen([os.path.join(self.cordova_app_folder, 'check_javac.bat')], stdout=subprocess.PIPE)
                    result_javac=javac.stdout.read()
                    path_javac=re_javac.findall(result_javac)
                    self.requeriments_store['javac']=path_javac
                except Exception as e:
                    print "Don't find javac in your system, try install JAVA SDK"
                    print e
            return self.requeriments_store
        elif  platform=='linux' or platform=='linux2':
            if update_req=='all' or update_req=='cordova':
                try:
                    cordova=subprocess.check_output(['which','cordova'])
                    cordova=cordova.strip().split('\n')[0]
                    self.requeriments_store['cordova']=cordova
                except Exception as e:
                    print "Don't find cordova in your system, try install. eg. npm install -g cordova"
                    print e
            if update_req=='all' or update_req=='phonegap':
                try:
                    phonegap=subprocess.check_output(['which','phonegap'])
                    phonegap=phonegap.strip().split('\n')[0]
                    self.requeriments_store['phonegap']=phonegap
                except Exception as e:
                    print "Don't find phonegap in your system, try install. eg. npm install -g phonegap"
                    print e
            if update_req=='all' or update_req=='keytool':
                try:
                    keytool=subprocess.check_output(['which','keytool'])
                    keytool=keytool.strip().split('\n')[0]
                    self.requeriments_store['keytool']=keytool
                except Exception as e:
                    print "Don't find keytool in your system, try install JAVA SDK"
                    print e  
            if update_req=='all' or update_req=='javac':
                try:
                    javac=subprocess.check_output(['which','javac'])
                    javac=javac.strip().split('\n')[0]
                    self.requeriments_store['javac']=javac
                except Exception as e:
                    print "Don't find javac in your system, try install JAVA SDK"
                    print e
            return self.requeriments_store


    def removeCordovaApp(self):
        request = self.request

        self.closeServer()
        print 'remove:', self.aplication_folder
        if os.path.exists(self.aplication_folder):
            try:
                shutil.rmtree(self.aplication_folder)
            except Exception as e:
                print "Erro on remove:", self.aplication_folder
                print e
        if platform == "win32" or platform == 'cygwin':
            self._remove_file(os.path.join(self.cordova_app_folder, 'create_app_%s.bat' % self.aplication_name))
            self._remove_file(os.path.join(self.cordova_app_folder, 'server_run_%s.bat' % self.aplication_name))
            self._remove_file(os.path.join(self.cordova_app_folder, 'create_apk_%s1.bat' % self.aplication_name))
            self._remove_file(os.path.join(self.cordova_app_folder, 'create_apk_%s2.bat' % self.aplication_name))
            self._remove_file(os.path.join(self.cordova_app_folder, 'create_apk_%s3.bat' % self.aplication_name))
    
    def createKeystore(self, keytool, 
        keyname="phantermobile", 
        aliasname='phantermobile', 
        validity=10000, 
        storepass='yourstorepasslarge',
        keypass='youkeypasslarge',
        CN='Your Name',
        OU='Departament',
        O='Organizacion',
        L='District',
        ST='State',
        C='BR'):
        kargs={
        'keytool':keytool, 
        'keyname':keyname,
        'aliasname':aliasname,
        'validity':validity,
        'storepass':storepass,
        'keypass':keypass,
        'CN':CN,
        'OU':OU,
        'O':O,
        'L':L,
        'ST':ST,
        'C':C,
        }
        keytool=keytool.replace('program files', 'progra~1').replace('Program Files', 'Progra~1')
        print keytool, "##############################################"
        args_keytool="-genkey -v -keystore %(keyname)s.keystore -alias %(aliasname)s "\
        "-keyalg RSA -keysize 2048 -validity %(validity)s -storepass %(storepass)s -keypass "\
        "%(keypass)s -dname \"CN=%(CN)s OU=%(OU)s O=%(O)s L=%(L)s ST=%(ST)s C=%(C)s\""
        if platform == "win32" or platform == 'cygwin':
            args_keytool_map=args_keytool %kargs
            with open(os.path.join(self.cordova_app_folder, 'create_key_%s.bat' % self.aplication_name), 'w') as arquivo_aberto:
                conteudo = "cd %s\n" %os.path.join(self.cordova_app_folder)
                complete_comand="%s %s" %(keytool, args_keytool_map)
                conteudo+=complete_comand
                arquivo_aberto.write(conteudo)
            print "creating keystore"
            subprocess.call([os.path.join(self.cordova_app_folder, 'create_key_%s.bat' %
                                          self.aplication_name)])
        elif platform == "linux" or platform == "linux2":
            print "creating keystore"
            if os.path.exists(os.path.join(self.cordova_app_folder, "%s.keystore" %keyname)):
                self._remove_file(os.path.join(self.cordova_app_folder, "%s.keystore" %keyname))

            subprocess.call('keytool %s' %args_keytool, cwd=self.cordova_app_folder, shell=True)
        print "Keystore saved in %s!" %self.cordova_app_folder
        self._created_key=[os.path.join(self.cordova_app_folder, "%s.keystore" %keyname), storepass, aliasname]
        return self._created_key

    def createApk(self, level="debug"):
        """
        @level: create apk debug if setted 'debug', create apk release if setted 'release'
        @include_key: is include in apk if keystore exists
        """
        self.buildHtml()
        if platform == "win32" or platform == 'cygwin':
            print "Creating file create_apk_%s3.bat" % self.aplication_name
            with open(os.path.join(self.cordova_app_folder, 'create_apk_%s3.bat' % self.aplication_name), 'w') as arquivo_aberto:
                conteudo = "cd %s\n" %os.path.join(self.aplication_folder)
                if level=='release':
                    if self._created_key:
                        conteudo+="cordova build android --verbose --release -- --keystore=\"%s\" --storePassword=%s --alias=%s" %(
                            self._created_key[0],self._created_key[1],self._created_key[2])
                    else:
                        conteudo+="cordova build android --verbose --release\n"
                else:
                    conteudo+="cordova build android --verbose\n"
                arquivo_aberto.write(conteudo)
            print "Creating APK file"
            subprocess.call([os.path.join(self.cordova_app_folder, 'create_apk_%s3.bat' %
                                          self.aplication_name)])
        elif platform == "linux" or platform == "linux2":
            if level=='release':
                if self._created_key:
                    subprocess.call(["cordova build android --verbose --release -- --keystore=\"%s\" --storePassword=%s --alias=%s" %(
                            self._created_key[0],self._created_key[1],self._created_key[2]
                        )], cwd=self.aplication_folder, shell=True)
                else:
                    subprocess.call(['cordova build android --verbose --release'], cwd=self.aplication_folder, shell=True)
            else:
                subprocess.call(['cordova build android --verbose'], cwd=self.aplication_folder, shell=True)
        print "Done!"


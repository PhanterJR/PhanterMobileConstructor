# -*- coding: utf-8 -*-
# versao: 1.2.0
import subprocess
import os
from gluon import template, SQLFORM
from gluon.html import *
from gluon import current
from gluon.compileapp import find_exposed_functions
import zipfile
import psutil
import urllib2
import shutil
import time

class PhanterAndroid(object):
    """docstring for processos"""
    def __init__(self):
        self.request=current.request
        self.aplicativo=self.request.application
        self.portas=[]
        self.porta=3000
        self.pasta_cordova=os.path.join(self.request.env.web2py_path, 'cordova')
        self.pasta_aplicativo=os.path.join(self.pasta_cordova, self.aplicativo)

        tem_condova=os.path.exists(self.pasta_cordova)
        tem_aplicativo=os.path.exists(self.pasta_aplicativo)
        if not tem_condova or not tem_aplicativo:
            self.prepararAmbiente(pre_build=True)

    def iniciarServidor(self):
        print "Iniciando servidor..."
        request=self.request
        
        procs=self._localizar_processos()
        if procs:
            self.porta=procs['porta']
            print 'servidor já está rodando na porta %s' %procs['porta']
        else:
            porta=3000
            for y in xrange(3000,4000):
                if y in self.portas:
                    pass
                else:
                    self.portas.append(y)
                    porta=y
                    break
            self.porta=porta
            with open(os.path.join(self.pasta_cordova,'server_run_%s.bat' %self.aplicativo), 'w') as arquivo_aberto:
                conteudo="cd %s\nphonegap serve -p%s" %(self.pasta_aplicativo, porta)
                arquivo_aberto.write(conteudo)                 

            processo=subprocess.Popen([os.path.join(self.pasta_cordova,'server_run_%s.bat' %self.aplicativo)], shell=False)
            proc=psutil.Process(processo.pid)
            while True:
                print "Tentando conectar...",
                if proc.children():
                    try:
                        urllib2.urlopen('http://localhost:%s' %porta)
                        break
                    except Exception as e:
                        print "Sem sucesso!" 
                        time.sleep(2)                  
                else:
                    time.sleep(1)      
            print "Concluído"
   
    def close(self):
        print "Fechando..."
        procs=self._localizar_processos()
        if procs:
            proc=psutil.Process(procs['pid'])
            proc.kill()
        else:
            print 'processo não localizado para fechar'

    def pre_build(self):
        request=self.request
        
        print "Compilando html..."
        self.close()

        origem=os.path.join(request.env.web2py_path, 'applications', self.aplicativo, 'static', 'plugin_phantermobileconstructor', 'www')
        self.lista_de_pastas_origem_e_destino=[]
        self.lista_de_pastas_destino=[]
        self.lista_de_arquivos_origem_e_destinos=[]
        self._verificar_pastas(origem)
        for y in self.lista_de_pastas_destino:
            if not os.path.exists(y):
                os.makedirs(y)
        for x in self.lista_de_arquivos_origem_e_destinos:
            shutil.copy(x[0], x[1])
        arquivo_plugin=os.path.join(request.env.web2py_path, 'applications', self.aplicativo, 'controllers', 'plugin_phantermobileconstructor.py')
        funcoes=[]
        with open(arquivo_plugin, 'r') as arquivo_aberto:
            funcoes = find_exposed_functions(arquivo_aberto.read())
        if funcoes:
            for x in (x for x in funcoes if x.startswith("www_")):
                url="%s?phantermobilebuild=True" %URL(c='plugin_phantermobileconstructor', f=x, host=True)
                print "tentando abrir: %s" %url
                cont=0
                nome_arquivo_html=x.replace('www_','')
                while cont<5:
                    try:
                        html_url=urllib2.urlopen(url)
                        html= html2 = html_url.read()
                        arquivo_destino=os.path.join(self.pasta_aplicativo, 'www', "%s.html" %nome_arquivo_html)
                        with open(arquivo_destino, 'w') as arquivo_aberto:
                            print 'copiando conteudo de %s para %s' %(url, arquivo_destino)
                            arquivo_aberto.write(html)
                        break
                    except Exception as e:
                        time.sleep(2)
                        print e
                        cont+=1
                        print "sem sucesso! tentativa %s de 5" %cont
                        
    def _localizar_processos(self):
        request=self.request
        print 'localizando processos...'
        nome='node.exe'
        processo_localizado={}
        processos_rodando={}
        for proc in psutil.process_iter():
            if proc.name() == nome:
                processos_rodando[proc.pid]={}
                if proc.parent():
                    processos_rodando[proc.pid]['parent']=proc.parent().pid
                else:
                    processos_rodando[proc.pid]['parent']=None
                porta_temp=proc.cmdline()[-1]
                if '-p' in porta_temp:
                    porta=porta_temp.split('-p')[-1].strip()
                    processos_rodando[proc.pid]['porta']=int(porta)
                    self.portas.append(int(porta))
                else:
                    processos_rodando[proc.pid]['porta']=3000
                processos_rodando[proc.pid]['pasta']=proc.cwd()
                if proc.cwd()==self.pasta_aplicativo:
                    processo_localizado['porta']=processos_rodando[proc.pid]['porta']
                    processo_localizado['pid']=proc.pid
                    print "\n================ SERVIDOR ==================\n Porta: %s\n Pasta:%s\n------------------------------------\n" %(processo_localizado['porta'], proc.cwd())
                else:
                    print "outro processo rodando na porta %s em %s" %(processos_rodando[proc.pid]['porta'], proc.cwd())

        return processo_localizado
                    

    def _verificar_pastas(self, path):
        request=self.request
        
        print "Verificando Pastas..."
        if not os.path.isfile(path):
            lista=os.listdir(path)
            if lista:
                for x in lista:
                    if not os.path.isfile(os.path.join(path, x)):
                        self.lista_de_pastas_destino.append(os.path.join(path.replace(os.path.join(request.env.web2py_path, 'applications', self.aplicativo, 'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.pasta_aplicativo, 'www')), x))
                        self.lista_de_pastas_origem_e_destino.append([os.path.join(path, x), 
                            os.path.join(path.replace(os.path.join(request.env.web2py_path, 'applications', self.aplicativo, 'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.pasta_aplicativo, 'www')), x), 
                            ])
                        self._verificar_pastas(os.path.join(path, x))
                    
                    else:
                        self.lista_de_arquivos_origem_e_destinos.append([os.path.join(path, x), 
                            os.path.join(path.replace(os.path.join(request.env.web2py_path, 'applications', self.aplicativo, 'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.pasta_aplicativo, 'www'))), 
                            ])
        else:
            self.lista_de_arquivos_origem_e_destinos.append([os.path.join(path), 
                os.path.join(path.replace(os.path.join(request.env.web2py_path, 'applications', self.aplicativo, 'static', 'plugin_phantermobileconstructor', 'www'), os.path.join(self.pasta_aplicativo, 'www'))), 
                ])

    def prepararAmbiente(self, pre_build=True):
        request=self.request
        
        print 'Preparando Ambiente'
        if not os.path.exists(self.pasta_cordova):
            print 'criando_pasta: %s' %self.pasta_cordova
            os.makedirs(self.pasta_cordova)       
        if not os.path.exists(os.path.join(self.pasta_cordova,'criar_aplicativo_%s.bat' %self.aplicativo)):
            print "criando arquivo de lote criar_aplicativo_%s.bat" %self.aplicativo
            with open(os.path.join(self.pasta_cordova,'criar_aplicativo_%s.bat' %self.aplicativo), 'w') as arquivo_aberto:
                conteudo="cd %s\ncordova create %s br.com.conexaodidata.%s %s" %(self.pasta_cordova, self.aplicativo, self.aplicativo, self.aplicativo)
                arquivo_aberto.write(conteudo)
        if not os.path.exists(self.pasta_aplicativo):
            print "criando pasta do aplicativo: %s" %self.pasta_aplicativo
            os.makedirs(self.pasta_aplicativo)
            print "executando o comando: cordova create %s br.com.conexaodidata.%s %s" %(self.aplicativo, self.aplicativo, self.aplicativo)
            subprocess.call([os.path.join(self.pasta_cordova,'criar_aplicativo_%s.bat' %self.aplicativo)], stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE)

        if not os.path.exists(os.path.join(self.pasta_aplicativo, 'www')):
            print "copiando template phanterandroid em: %s" %os.path.join(self.pasta_aplicativo, 'www')
            print "desconpactando template localizado em: %s" %os.path.abspath(os.path.join(os.path.dirname(__file__), 'phanterandroidpack','template.zip'))
            zip_ref = zipfile.ZipFile(os.path.abspath(os.path.join(os.path.dirname(__file__), 'phanterandroidpack','template.zip')), 'r')
            zip_ref.extractall(os.path.join(self.pasta_aplicativo, 'www'))
            zip_ref.close()
        if pre_build:
            self.pre_build()
            
    def reset(self):
        request=self.request
        
        self.close()
        if os.path.exists(self.pasta_aplicativo):
            shutil.rmtree(self.pasta_aplicativo)
            self.prepararAmbiente(pre_build=False)

    def deletar_app(self):
        request=self.request
        
        self.close()
        print 'removendo:', self.pasta_aplicativo
        if os.path.exists(self.pasta_aplicativo):
            try:
                shutil.rmtree(self.pasta_aplicativo)
            except Exception as e:
                print "Erro ao apagar:", self.pasta_aplicativo
                print e
        if os.path.exists(os.path.join(self.pasta_cordova,'criar_aplicativo_%s.bat' %self.aplicativo)):
            try:
                os.unlink(os.path.join(self.pasta_cordova,'criar_aplicativo_%s.bat' %self.aplicativo))
            except Exception as e:
                print "Erro ao apagar:", os.path.join(self.pasta_cordova,'criar_aplicativo_%s.bat' %self.aplicativo)
                print e
        if os.path.exists(os.path.join(self.pasta_cordova,'server_run_%s.bat' %self.aplicativo)):
            try:
                os.unlink(os.path.join(self.pasta_cordova,'server_run_%s.bat' %self.aplicativo))
            except Exception as e:
                print "Erro ao apagar:", os.path.join(self.pasta_cordova,'server_run_%s.bat' %self.aplicativo)
                print e

def phanterURL(*args, **kargs):
    if current.request.vars.phanterandroidbuild:
        kargs['host']=True
        url='%s' %URL(*args, **kargs)
        if current.request.application in url:
            url_split=url.split('%s/' %current.request.application)
            return '%s' %url_split[-1]
        else:
            return ''
    else:
        return URL(*args, **kargs)
        

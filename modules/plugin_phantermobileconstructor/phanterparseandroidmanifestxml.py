# -*- coding: utf-8 -*-
# python3 compatibility
from __future__ import unicode_literals

from unicodedata import normalize
from io import open
import xml.etree.ElementTree as ET
import os
import re


class parseAndroidManifestXML(object):
    """docstring for parseAndroidManifestXML"""
    def __init__(self, arquivo):
        super(parseAndroidManifestXML, self).__init__()
        self.arquivo = arquivo
        self.tree = ET.parse(self.arquivo)
        self.root = self.tree.getroot()
        elements={}

    def addElementRoot(self, element, atribute, value_atribute):

        position=1
        last_position=0
        element_exists=False
        for x in self.root:
            elementname="%s" %(element)

            if elementname == x.tag:
                atribute="%s%s" %(self._prefixmlns ,atribute)
                print(atribute, x.attrib, atribute in x.attrib)
                if atribute in x.attrib:
                    if x.attrib[atribute]==value_atribute:
                        element_exists=True
                last_position=position
            position=position+1

        new_element=ET.Element(element)
        new_element.set(atribute, removedordeacentosp2e3(value_atribute))
        if not element_exists:
            if last_position:
                self.root.insert(last_position, new_element)
            else:
                self.root.append(new_element)

    def removeElementRoot(self, element, atribute=None, value_atribute=None):
        elements_to_remove=[]
        for x in self.root:
            elementname=element
            if elementname==x.tag:
                if atribute:
                    atribute="%s%s" %(self._prefixmlns ,atribute)
                    if atribute in x.attrib:
                        if value_atribute:
                            if value_atribute==x.attrib[atribute]:
                                self.root.remove(x)
                        else:
                            self.root.remove(x)
                else:
                    self.root.remove(x)

    @property
    def _prefixmlns(self):
        comp=re.compile(r'{http.+?}')
        prefix=comp.findall(self.root.attrib.keys()[0])
        return prefix[0]

    def write(self, local):
        self.tree.write(local)
        with open(local, 'r') as f:
            arquivo=f.read()

        with open(local, 'w') as f2:
            #print(arquivo)
            #print(self._prefixmlns)
            cabecalho='<?xml version=\'1.0\' encoding=\'utf-8\'?>\n'
            arquivo=cabecalho+arquivo
            arquivo=arquivo.replace(':ns0',':android').replace('ns0:','android:').replace('/><', '/>\n    <').replace('/>\n<', '/>\n    <').replace('    </manifest>','</manifest>')
            f2.write(arquivo)
            
    def save(self):
        self.write(self.arquivo)


def removedordeacentosp2e3(palavra):
    try:
        #python3
        p_sem_acento=normalize('NFKD', palavra).encode('ASCII','ignore').decode('utf-8')
    except TypeError:
        #python2
        p_sem_acento = normalize('NFKD', palavra.decode('utf-8')).encode('ASCII','ignore')
    return p_sem_acento

if __name__ == '__main__':
    teste=parseAndroidManifestXML(os.path.join(r'C:\web2py_latest\cordova\welcome\platforms\android', 'AndroidManifest.xml'))
    
    teste.write(os.path.join(r'C:\web2py_latest\cordova\welcome\platforms\android', 'AndroidManifest2.xml'))

# -*- coding: utf-8 -*-
# python3 compatibility
from __future__ import unicode_literals

from unicodedata import normalize
from io import open
import xml.etree.ElementTree as ET
import os
import re


class parseConfigXML(object):
    """docstring for parseConfigXML"""
    def __init__(self, arquivo):
        super(parseConfigXML, self).__init__()
        self.arquivo = arquivo
        self.tree = ET.parse(self.arquivo)
        self.root = self.tree.getroot()
        elements={}

    def checkEngine(self, platform='android'):
        for x in self.root:
            if x.tag.split(self._prefixmlns)[1] == 'engine':
                if x.attrib:
                    if 'name' in x.attrib.keys():
                        if x.attrib['name']==platform:
                            return True
        return False

    def checkPlugin(self, plugin):
        for x in self.root:
            if x.tag.split(self._prefixmlns)[1] == 'plugin':
                if x.attrib:
                    if 'name' in x.attrib.keys():
                        if x.attrib['name']==plugin:
                            return True
        return False

    def checkNeedInternet(self):
        need=False
        for x in self.root:
            tag=x.tag.split(self._prefixmlns)[1]
            if tag == 'access' or tag == 'allow-navigatio':
                need=True
        return need


    def _changeText(self, element, new_text):
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, element)
            if elementname == x.tag:
                x.text=removedordeacentosp2e3(new_text)

    def _changeatribute(self, element, atribute, value_atribute):
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, element)
            if elementname == x.tag:
                x.set(atribute, removedordeacentosp2e3(value_atribute))

    def _changelementlist(self, element, atribute, old_value, new_value):
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, element)
            if elementname == x.tag:
                if (atribute in x.attrib) and (old_value==x.get(x.attrib)):
                    x.set(atribue, removedordeacentosp2e3(new_value))
    
    def _gettext(self, element):
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, element)
            if elementname == x.tag:
                return x.text

    def _getatributevalue(self, element, atribute):
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, element)
            if (elementname == x.tag) and (atribute in x.attrib):
                return x.attrib[atribute]

    def addElementRoot(self, element, atribute, value_atribute):
        position=1
        last_position=0
        element_exists=False
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, element)
            if elementname == x.tag:
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
            elementname="%s%s" %(self._prefixmlns, element)
            if elementname==x.tag:
                if atribute:
                    if atribute in x.attrib:
                        if value_atribute:
                            if value_atribute==x.attrib[atribute]:
                                self.root.remove(x)
                        else:
                            self.root.remove(x)
                else:
                    self.root.remove(x)


    def addIcons(self):
        for x in self.root:
            elementname="%s%s" %(self._prefixmlns, 'platform')
            if elementname == x.tag:
                if 'name' in x.attrib:
                    if x.attrib['name']=='android':
                        ldpi=False
                        mdpi=False
                        hdpi=False
                        xhdpi=False
                        xxhdpi=False
                        xxxhdpi=False
                        for y in x:
                            elementnameY="%s%s" %(self._prefixmlns, 'icon')
                            if elementnameY==y.tag:
                                if 'density' in y.attrib:
                                    if y.attrib['density']=='ldpi':
                                        ldpi=True
                                        if 'src' in y.attrib:
                                            y.attrib['src']='res/icon/android/icon-36-ldpi.png'
                                        else:
                                            y.set('src', 'res/icon/android/icon-36-ldpi.png')
                                    elif y.attrib['density']=='mdpi':
                                        mdpi=True
                                        if 'src' in y.attrib:
                                            y.attrib['src']='res/icon/android/icon-48-mdpi.png'
                                        else:
                                            y.set('src', 'res/icon/android/icon-48-mdpi.png')
                                    elif y.attrib['density']=='hdpi':
                                        hdpi=True
                                        if 'src' in y.attrib:
                                            y.attrib['src']='res/icon/android/icon-72-hdpi.png'
                                        else:
                                            y.set('src', 'res/icon/android/icon-72-hdpi.png')
                                    elif y.attrib['density']=='xhdpi':
                                        xhdpi=True
                                        if 'src' in y.attrib:
                                            y.attrib['src']='res/icon/android/icon-96-xhdpi.png'
                                        else:
                                            y.set('src', 'res/icon/android/icon-96-xhdpi.png')
                                    elif y.attrib['density']=='xxhdpi':
                                        xxhdpi=True
                                        if 'src' in y.attrib:
                                            y.attrib['src']='res/icon/android/icon-144-xxhdpi.png'
                                        else:
                                            y.set('src', 'res/icon/android/icon-144-xxhdpi.png')
                                    elif y.attrib['density']=='xxxhdpi':
                                        xxxhdpi=True
                                        if 'src' in y.attrib:
                                            y.attrib['src']='res/icon/android/icon-192-xxxhdpi.png'
                                        else:
                                            y.set('src', 'res/icon/android/icon-192-xxxhdpi.png')
                        if not ldpi:
                            new_element=ET.Element('icon')
                            new_element.set('src', 'res/icon/android/icon-36-ldpi.png')
                            new_element.set('density', 'ldpi')
                            x.append(new_element)
                        if not mdpi:
                            new_element=ET.Element('icon')
                            new_element.set('src', 'res/icon/android/icon-48-mdpi.png')
                            new_element.set('density', 'mdpi')
                            x.append(new_element)
                        if not hdpi:
                            new_element=ET.Element('icon')
                            new_element.set('src', 'res/icon/android/icon-72-hdpi.png')
                            new_element.set('density', 'hdpi')
                            x.append(new_element)
                        if not xhdpi:
                            new_element=ET.Element('icon')
                            new_element.set('src', 'res/icon/android/icon-96-xhdpi.png')
                            new_element.set('density', 'xhdpi')
                            x.append(new_element)
                        if not xxhdpi:
                            new_element=ET.Element('icon')
                            new_element.set('src', 'res/icon/android/icon-144-xxhdpi.png')
                            new_element.set('density', 'xxhdpi')
                            x.append(new_element)
                        if not xxxhdpi:
                            new_element=ET.Element('icon')
                            new_element.set('src', 'res/icon/android/icon-192-xxxhdpi.png')
                            new_element.set('density', 'xxxhdpi')
                            x.append(new_element)

    def addSplash(self, portrait=False):
        preference=False
        for x in self.root:
            elementnamepreference="%s%s" %(self._prefixmlns, 'preference')
            if elementnamepreference == x.tag:
                if 'name' in x.attrib:
                    if x.attrib['name']=='SplashScreenDelay':
                        preference=True
            elementname="%s%s" %(self._prefixmlns, 'platform')
            if elementname == x.tag:
                if 'name' in x.attrib:
                    if x.attrib['name']=='android':
                        land_ldpi=False
                        land_mdpi=False
                        land_hdpi=False
                        land_xhdpi=False
                        land_xxhdpi=False
                        land_xxxhdpi=False
                        port_ldpi=False
                        port_mdpi=False
                        port_hdpi=False
                        port_xhdpi=False
                        port_xxhdpi=False
                        port_xxxhdpi=False
                        for y in x:
                            elementnameY="%s%s" %(self._prefixmlns, 'splash')
                            if elementnameY==y.tag:
                                if 'density' in y.attrib:
                                    if portrait:
                                        if y.attrib['density']=='port-ldpi':
                                            port_ldpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-ldpi-portrait.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-ldpi-portrait.png')
                                        elif y.attrib['density']=='port-mdpi':
                                            port_mdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-mdpi-portrait.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-mdpi-portrait.png')
                                        elif y.attrib['density']=='port-hdpi':
                                            port_hdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-hdpi-portrait.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-hdpi-portrait.png')
                                        elif y.attrib['density']=='port-xhdpi':
                                            port_xhdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-xhdpi-portrait.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-xhdpi-portrait.png')
                                        elif y.attrib['density']=='port-xxhdpi':
                                            port_xxhdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-xxhdpi-portrait.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-xxhdpi-portrait.png')
                                        elif y.attrib['density']=='port-xxxhdpi':
                                            port_xxxhdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-xxxhdpi-portrait.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-xxxhdpi-portrait.png')
                                    else:
                                        if y.attrib['density']=='land-ldpi':
                                            land_ldpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-ldpi-landscape.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-ldpi-landscape.png')
                                        elif y.attrib['density']=='land-mdpi':
                                            land_mdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-mdpi-landscape.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-mdpi-landscape.png')
                                        elif y.attrib['density']=='land-hdpi':
                                            land_hdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-hdpi-landscape.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-hdpi-landscape.png')
                                        elif y.attrib['density']=='land-xhdpi':
                                            land_xhdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-xhdpi-landscape.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-xhdpi-landscape.png')
                                        elif y.attrib['density']=='land-xxhdpi':
                                            land_xxhdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-xxhdpi-landscape.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-xxhdpi-landscape.png')
                                        elif y.attrib['density']=='land-xxxhdpi':
                                            land_xxxhdpi=True
                                            if 'src' in y.attrib:
                                                y.attrib['src']='res/screen/android/screen-xxxhdpi-landscape.png'
                                            else:
                                                y.set('src', 'res/screen/android/screen-xxxhdpi-landscape.png')
                        if portrait:
                            if not port_ldpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-ldpi-portrait.png')
                                new_element.set('density', 'port-ldpi')
                                x.append(new_element)
                            if not port_mdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-mdpi-portrait.png')
                                new_element.set('density', 'port-mdpi')
                                x.append(new_element)
                            if not port_hdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-hdpi-portrait.png')
                                new_element.set('density', 'port-hdpi')
                                x.append(new_element)
                            if not port_xhdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-xhdpi-portrait.png')
                                new_element.set('density', 'port-xhdpi')
                                x.append(new_element)
                            if not port_xxhdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-xxhdpi-portrait.png')
                                new_element.set('density', 'port-xxhdpi')
                                x.append(new_element)
                            if not port_xxxhdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-xxxhdpi-portrait.png')
                                new_element.set('density', 'port-xxxhdpi')
                                x.append(new_element)
                        else:
                            if not land_ldpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-ldpi-landscape.png')
                                new_element.set('density', 'land-ldpi')
                                x.append(new_element)
                            if not land_mdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-mdpi-landscape.png')
                                new_element.set('density', 'land-mdpi')
                                x.append(new_element)
                            if not land_hdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-hdpi-landscape.png')
                                new_element.set('density', 'land-hdpi')
                                x.append(new_element)
                            if not land_xhdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-xhdpi-landscape.png')
                                new_element.set('density', 'land-xhdpi')
                                x.append(new_element)
                            if not land_xxhdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-xxhdpi-landscape.png')
                                new_element.set('density', 'land-xxhdpi')
                                x.append(new_element)
                            if not land_xxxhdpi:
                                new_element=ET.Element('splash')
                                new_element.set('src', 'res/screen/android/screen-xxxhdpi-landscape.png')
                                new_element.set('density', 'land-xxxhdpi')
                                x.append(new_element)

        if not preference:
            '<preference name="SplashScreenDelay" value="10000" />'
            new_elementpreference=ET.Element('preference')
            new_elementpreference.set('name', 'SplashScreenDelay')
            new_elementpreference.set('value', '10000')
            self.root.append(new_elementpreference)
            
    @property
    def _prefixmlns(self):
        return "%s}" %self.root.tag.split('}widget')[0]

    @property
    def appname(self):
        return self._gettext('name')

    @appname.setter
    def appname(self, value):
        self._changeText('name', value)
    
    @property
    def description(self):
        return self._gettext('description')

    @description.setter
    def description(self, value):
        self._changeText('description', value)


    @property
    def authorname(self):
        return self._gettext('author')

    @authorname.setter
    def authorname(self, value):
        self._changeText('author', value)

    @property
    def apkversion(self):
        return self.root.attrib['version']
    
    @apkversion.setter
    def apkversion(self, value):
        self.root.set('version', removedordeacentosp2e3(value))

    @property
    def idapp(self):
        return self.root.attrib['id']
    
    @idapp.setter
    def idapp(self, value):
        self.root.set('id', removedordeacentosp2e3(value))

    @property
    def authoremail(self):
        return self._getatributevalue('author', 'email')
    
    @authoremail.setter
    def authoremail(self, value):
        self._changeatribute('author', 'email', value)

    @property
    def authorwebsite(self):
        return self._getatributevalue('author', 'href')

    @authorwebsite.setter
    def authorwebsite(self, value):
        self._changeatribute('author', 'href', value)

    def write(self, local):
        self.tree.write(local)
        with open(local, 'r') as f:
            arquivo=f.read()

        with open(local, 'w') as f2:
            arquivo=arquivo.replace('ns0:','').replace('/><', '/>\n    <').replace('/>\n<', '/>\n    <').replace('    </widget>','</widget>')
            com=re.compile(r'<widget.+>')
            com2=re.compile(r'\n    <icon ')
            arquivo=com2.sub('\n        <icon ', arquivo)
            com3=re.compile(r'\n    <screen ')
            arquivo=com3.sub('\n        <screen ', arquivo)
            cabecalho='<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<widget id="%s" version="%s" xmlns="%s" xmlns:cdv="http://cordova.apache.org/ns/1.0">' %(self.idapp, self.apkversion, self._prefixmlns.replace('{','').replace('}',''))
            arquivo=com.sub(cabecalho, arquivo)
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

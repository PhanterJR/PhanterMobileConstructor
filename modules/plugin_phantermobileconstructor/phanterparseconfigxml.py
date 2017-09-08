# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os


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


	def _changeText(self, element, new_text):
		for x in self.root:
			elementname="%s%s" %(self._prefixmlns, element)
			if elementname == x.tag:
				x.text=new_text

	def _changeatribute(self, element, atribute, value_atribute):
		for x in self.root:
			elementname="%s%s" %(self._prefixmlns, element)
			if elementname == x.tag:
				x.set(atribute, value_atribute)


	def _changelementlist(self, element, atribute, old_value, new_value):
		for x in self.root:
			elementname="%s%s" %(self._prefixmlns, element)
			if elementname == x.tag:
				if (atribute in x.attrib) and (old_value==x.get(x.attrib)):
					x.set(atribue, new_value)
	
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

	def addElementList(self, element, atribute, value_atribute):
		position=0
		last_position=0
		element_exists=False
		for x in self.root:
			elementname="%s%s" %(self._prefixmlns, element)
			if elementname == x.tag:
				last_position=position
			position=position+1

		new_element=ET.Element(element)
		new_element.set(atribute, value_atribute)
		if last_position and not element_exists:
			self.root.insert(last_position+1, new_element)
		else:
			self.root.insert(position, new_element)
				
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
		self.root.set('version', value)

	@property
	def idapp(self):
		return self.root.attrib['id']
	
	@idapp.setter
	def idapp(self, value):
		self.root.set('id',value)

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
		cabecalho='<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<widget id="%s" version="%s" xmlns="%s" xmlns:cdv="http://cordova.apache.org/ns/1.0">' %(self.idapp, self.apkversion, self._prefixmlns.replace('{','').replace('}',''))
		import StringIO
		output = StringIO.StringIO()
		self.tree.write(output)
		lines=output.getvalue().split('\n')
		lines[0]=cabecalho
		text= '\n'.join(lines).replace('ns0:','').replace('/><', '/>\n    <').replace('/>\n<', '/>\n    <').replace('    </widget>','</widget>')
		with open(local, 'w') as arquivo_aberto:
			arquivo_aberto.write(text.strip())

	def save(self):
		cabecalho='<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<widget id="%s" version="%s" xmlns="%s" xmlns:cdv="http://cordova.apache.org/ns/1.0">' %(self.idapp, self.apkversion, self._prefixmlns.replace('{','').replace('}',''))
		import StringIO
		output = StringIO.StringIO()
		self.tree.write(output)
		lines=output.getvalue().split('\n')
		lines[0]=cabecalho
		text= '\n'.join(lines).replace('ns0:','').replace('/><', '/>\n    <').replace('/>\n<', '/>\n    <').replace('    </widget>','</widget>')
		with open(self.arquivo, 'w') as arquivo_aberto:
			arquivo_aberto.write(text.strip())


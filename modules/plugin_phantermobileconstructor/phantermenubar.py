# -*- coding: utf-8 -*-
from gluon import template, SQLFORM
from gluon.html import *
from gluon import current

class PhanterMenubar(object):
    """docstring for PhanterMenu"""
    def __init__(self, *args, **kargs):
        super(PhanterMenubar, self).__init__()
        self.args=args
        self.kargs=kargs
    def xml(self):
        return "%s" %(TAG['nav'](*self.args, **self.kargs))
    def __str__(self):
        """
        str(COMPONENT) returns COMPONENT.xml()
        """
        return self.xml()

class PhanterMenu(object):
    """docstring for PhanterMenu"""
    def __init__(self, menu, **kargs):
        super(PhanterMenu, self).__init__()
        self.menu = menu
        self.kargs=""
        self.itens=""
        if kargs:
            self.kargs=kargs_sintetize(kargs)   
    def addItem(self, *args, **kargs2):
        self.args=args
        self.itens+="%s" %(LI(*self.args, **kargs2))
    def xml(self):
        if not self.itens:
            return "%s" %(DIV(self.menu, **self.kargs))
        else:
            return "%s" %(DIV(self.menu, UL(self.itens), **self.kargs))
    def __str__(self):
        """
        str(COMPONENT) returns COMPONENT.xml()
        """
        return self.xml()
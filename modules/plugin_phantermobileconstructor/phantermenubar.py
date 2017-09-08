# -*- coding: utf-8 -*-
from gluon.html import *


class PhanterMenubar(object):
    """Helper to construct the menubar"""

    def __init__(self, *args, **kargs):
        super(PhanterMenubar, self).__init__()
        self.args = args
        self.kargs = kargs

    def xml(self):
        return "%s" % (TAG['nav'](*self.args, **self.kargs))

    def __str__(self):
        return self.xml()
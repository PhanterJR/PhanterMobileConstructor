# -*- coding: utf-8 -*-
# python 3 comtability
from __future__ import print_function

import os

# this import need install (battery dont incluided)
from PIL import Image as PilImage



class RECOMMENDED_MIN_SIZE(object):

    def __init__(self, nx='', ny='', error_message='Enter a value'):
        self.error_message = error_message
        self.nx=nx
        self.ny=ny

    def __call__(self, value):
        if isinstance(value, str) and len(value) == 0:
            return (value, None)
        try:
            t_value=value
            print(dir(t_value))
            img = PilImage.open(t_value.file)
            x = img.size[0]
            y = img.size[1]
        except Exception as e:
            print('error:', e)
            return (value, self.error_message)

        if x<self.nx or y<self.ny:
            return (value, self.error_message)
        else:
            return (value, None)

class IS_PNG(object):

    def __init__(self, error_message=' image resize'):
        self.error_message = error_message

    def __call__(self, value):

        if isinstance(value, str) and len(value) == 0:
            return (value, None)
        extensao = os.path.splitext(value.filename)[1]
        if extensao == ".png" or extensao == ".PNG":
            print('extensao',extensao)
            return (value, None)
        else:
            return (value, self.error_message)
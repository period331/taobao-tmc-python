# coding: utf-8

class Shop(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', '')
        self.session = kwargs.pop('session', '')

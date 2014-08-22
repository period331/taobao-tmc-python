#coding: utf-8

from collections import defaultdict

class InvalidListenerError(Exception): pass

class DuplicateListenerError(Exception): pass

class Event(object):
    def __init__(self, *args, **kwargs):
        self.__listeners = defaultdict(list)

    def on(self, name, callback):
        assert callable(callback), 'callback is not callable.'
        if callback in self.__listeners[name]:
            raise DuplicateListenerError()

        self.__listeners[name].append(callback)

    def off(self, name, callback):
        if callback not in self.__listeners[name]:
            raise InvalidListenerError()

        self.__listeners[name].remove(callback)

    def fire(self, name, *args, **kwargs):
        for ev in self.__listeners[name]:
            ev(*args, **kwargs)


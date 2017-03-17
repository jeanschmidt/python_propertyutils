# -*- coding: utf-8 -*-

##############################################################################
# File:        classproperty.py
# Author:      Jean Schmidt <jean.schmidt@pollux.com.br>
# Description: create the classproperty decorator
##############################################################################

from __future__ import unicode_literals


class ClassPropertyDescriptor(object):
    """
    Thanks StackOverflow =)
    """
    def __init__(self, fget, fset=None, fdel=None):
        if not isinstance(fget, (classmethod, staticmethod)):
            fget = classmethod(fget)

        if not isinstance(fset, (classmethod, staticmethod)):
            fset = classmethod(fset)

        if not isinstance(fdel, (classmethod, staticmethod)):
            fdel = classmethod(fdel)

        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        type_ = type(obj)
        return self.fdel.__get__(obj, type_)()

    def getter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fget = func
        return self

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self

    def deleter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fdel = func
        return self


def classproperty(fget, fset=None, fdel=None):
    return ClassPropertyDescriptor(fget=fget, fset=fset, fdel=fdel)

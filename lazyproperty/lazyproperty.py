# -*- coding: utf-8 -*-

##############################################################################
# File:        lazyproperty.py
# Author:      Jean Schmidt <jean.schmidt@pollux.com.br>
# Created On:  09:56 27/10/16
##############################################################################

from __future__ import unicode_literals
from .classproperty import ClassPropertyDescriptor


def _xfget(name, fget):
    def xfget(self):
        if not hasattr(self, name):
            setattr(self, name, fget(self))
        return getattr(self, name)
    return xfget


def _xfset(name, fset):
    def xfset(self, val):
        if fset is not True:
            val = fset(self, val)
        setattr(self, name, val)
    return xfset


def _xfdel(name, fdel):
    def xfdel(self):
        if fdel is not True:
            fdel(self)
        else:
            if hasattr(self, name):
                delattr(self, name)
    return xfdel


def metalazyproperty(propertyclass):
    def lazypropertyfn(name=None, fset=None, fdel=None):
        """
        How to use:

        - Creates a property called 'myprop', internally stored as '_myprop',
        that is instantiaded only once, read only, and return the value
        'DefaultValue()'

        @lazyproperty('_myprop')
        def myprop(self):
            return DefaultValue()

        self.myprop == <instance DefaultValue>

        - Optionaly, the store name can be ommited, in this case the name used
        to store the value will be the name given for this property with a '_'
        (underscore) in front of it. The code bellow creates exactly the same
        property (with the same persistence name used) as the code above:

        @lazyproperty()
        def myprop(self):
            return DefaultValue()

        self.myprop == <instance DefaultValue>

        - Creates a property called 'myprop2', internally stored as '_myprop2',
        that acepts being set, but, if no value is given to it, it returns
        'DefaultValue()', and can be deleted, with causes it to return its default
        value

        @lazyproperty('_myprop2', fset=True, fdel=True)
        def myprop2(self):
            return DefaultValue()

        self.myprop2 == DefaultValue()
        self.myprop2 = 10
        self.myprop2 == 10
        del self.myprop2
        self.myprop2 == DefaultValue()

        - Creates a property called myprop3, internally stored as '_FOO',
        that accepts being set but only if is 'basestring', then append a string
        at the end. It also cannot be deleted.

        def myprop3(self, value):
            if not isinstance(value, basestring):
                raise Exception('NOOOO')
            return value + ' software engineer @Pollux'

        @lazyproperty('_FOO', fset=True, fdel=True)
        def myprop3(self):
            return 'No one'

        self.myprop3 == 'No one'
        self.myprop3 = 'Jean Schmidt'
        self.myprop3 == 'Jean Schmidt software engineer @Pollux'
        self.myprop3 = 10
        Traceback(....)
        del self.myprop3
        Traceback(....)
        self.myprop3 == 'Jean Schmidt software engineer @Pollux'
        """
        def decor(fget, fset=fset, fdel=fdel, name=name):
            if name is None:
                name = '_' + fget.__name__

            if not isinstance(name, basestring):
                raise Exception('name given to lazypropertyfn should be a '
                                'valid python string!')

            return propertyclass(
                name=name,
                fget=_xfget(name, fget),
                fset=(_xfset(name, fset) if fset is not None else None),
                fdel=(_xfdel(name, fdel) if fdel is not None else None)
            )

        return decor
    return lazypropertyfn


class _MetaLazyProperty(object):
    def getter(self, fn):
        return self.__class__(
            self._name,
            fget=_xfget(self._name, fn),
            fset=self.fset,
            fdel=self.fdel,
        )

    def setter(self, fn):
        return self.__class__(
            self._name,
            fget=self.fget,
            fset=_xfget(self._name, fn),
            fdel=self.fdel,
        )

    def deletter(self, fn):
        return self.__class__(
            self._name,
            fget=self.fget,
            fset=self.fset,
            fdel=_xfdel(self._name, fn),
        )


class _LazyPropertyDescriptor(_MetaLazyProperty, property):
    def __init__(self, name, *args, **kwargs):
        self._name = name
        property.__init__(self, *args, **kwargs)


class _LazyClassPropertyDescriptor(_MetaLazyProperty, ClassPropertyDescriptor):
    def __init__(self, name, *args, **kwargs):
        self._name = name
        ClassPropertyDescriptor.__init__(self, *args, **kwargs)


lazyproperty = metalazyproperty(_LazyPropertyDescriptor)
lazyclassproperty = metalazyproperty(_LazyClassPropertyDescriptor)

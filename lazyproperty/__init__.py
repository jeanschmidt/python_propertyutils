# -*- coding: utf-8 -*-

##############################################################################
# File:        __init__.py
# Author:      Jean Schmidt <jean.schmidt@pollux.com.br>
# Created On:  15:34 17/03/17
##############################################################################

from __future__ import unicode_literals

from .lazyproperty import lazyproperty, lazyclassproperty
from .classproperty import classproperty


__all__ = [
    'lazyproperty',
    'lazyclassproperty',
    'classproperty',
]


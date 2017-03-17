# -*- coding: utf-8 -*-

##############################################################################
# File:        setup.py
# Author:      Jean Schmidt <jean.schmidt@pollux.com.br>
# Created On:  15:37 17/03/17
##############################################################################

from __future__ import print_function
from __future__ import unicode_literals

import setuptools


setuptools.setup(
    name='lazyproperty',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/jeanschmidt/python_propertyutils.git',
    license='MIT',
    author='Jean Schmidt',
    author_email='contact@jschmidt.me',
    description='A really verbose stack to make properties lazy'
)

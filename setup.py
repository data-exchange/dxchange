#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='dxchange',
    author='Doga Gursoy, Francesco De Carlo',
    packages=find_packages(),
    version=open('VERSION').read().strip(),
    description = 'Readers for tomographic data files collected at different facilities.',
    license='BSD',
    platforms='Any'
)

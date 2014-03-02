#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import platform
import warnings

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, Extension, find_packages

# Check Python packages.
try:
    import numpy
except ImportError:
    raise ImportError("tomopy requires numpy 1.8.0 (hint: pip install numpy)")
try:
    import h5py
except ImportError:
    raise ImportError("tomopy requires h5py 2.2.1 (hint: pip install h5py)")

# Main setup configuration.
setup(
        name='data-exchange',
        version='0.0.1',

        packages = find_packages(),
        
        # include_package_data = True,

        # Specify C/C++ file paths. They will be compiled and put into tomopy.lib:
        # ext_modules=[ext_fftw, ext_gridrec],

        author='Francesco De Carlo',
        author_email='decarlo@aps.anl.gov',

        description='Data Exchange Toolbox',
        keywords=['tomography', 'data', 'format'],
        url='http://aps.anl.gov/DataExchange',
        download_url='http://github.com/data-exchange/data-exchange',

        license='BSD',
        platforms='Any',

        classifiers=['Development Status :: 1 - Beta',
                     'License :: OSI Approved :: BSD License',
                     'Intended Audience :: Science/Research',
                     'Intended Audience :: Education',
                     'Intended Audience :: Developers',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7']
)

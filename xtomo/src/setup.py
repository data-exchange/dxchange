from __future__ import print_function

from distutils.core import setup
from distutils.extension import Extension

setup(
    author = 'Francesco De Carlo, Argonne National Laboratory',
    description = 'Tomography data exchange toolbox',
    py_modules = ['xtomo_importer', 'xtomo_reader' , 'xtomo_exporter' , 'colorer'],
    name = 'xtomo',
    requires = (
        'python',
        ),
    version = '1.0',
)

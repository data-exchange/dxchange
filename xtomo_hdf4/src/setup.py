from __future__ import print_function

from distutils.core import setup
from distutils.extension import Extension

setup(
    author = 'Francesco De Carlo, Argonne National Laboratory',
    description = 'Tomography data exchange toolbox',
    py_modules = ['xtomo_hdf4_importer', 'xtomo_hdf4_reader' , 'xtomo_hdf4_exporter' , 'colorer'],
    name = 'xtomo_hdf4',
    requires = (
        'python',
        ),
    version = '1.0',
)

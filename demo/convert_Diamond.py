# -*- coding: utf-8 -*-
"""
.. module:: convert_Diamond.py
   :platform: Unix
   :synopsis: Convert Diamond NeXuS files in data exchange.

Example on how to use the `xtomo_raw`_ module to read Diamond NeXuS raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

#import numpy as np
#import os
#import scipy
#import re

import logging
logging.basicConfig(filename='convert_Diamond_I12.log',level=logging.DEBUG)

def main():

    file_name = '/local/dataraid/databank/Diamond/13429_subx.nxs'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Diamond_04.h5'

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name, 
                                                        data_type='nxs', 
                                                        slices_start=1600,
                                                        slices_end=1610,
                                                        slices_step=1,
                                                        log='INFO')
    
    
    # Save data as dataExchange
    write = dataexchange.Export()
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections')

if __name__ == "__main__":
    main()


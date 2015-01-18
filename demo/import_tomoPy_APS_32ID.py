# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_yecko.py
   :platform: Unix
   :synopsis: Import APS 32-ID TIFF files in tomoPy

Example on how to use the `xtomo_raw`_ module to read APS 32-ID TIFF raw tomographic data and reconstruct using tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.11.19

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

import re

def main():

    file_name = '/local/dataraid/2014_11/yecko/Sam01/test_.tif'

    dark_start = 1
    dark_end = 6
    dark_step = 1
    white_start = 6
    white_end = 11
    white_step = 1
    projections_start = 11
    projections_end = 1512

    # to reconstruct a subset of slices set slices_start and slices_end
    # if omitted the full data set is recontructed
    
    slices_start = 800    
    slices_end = 804    

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name = file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       projections_zeros = True,
                                                       projections_digits = 5,
                                                       log='INFO'
                                                       )

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=658.5
    d.gridrec()


    # Write to stack of TIFFs.
    write = dataexchange.Export()
    write.xtomo_tiff(d.data_recon, '/local/dataraid/2014_11/yecko/Sam01/rec/test_', axis=0)

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_15ID.py
   :platform: Unix
   :synopsis: Import APS 15ID hdf5 NeXuS files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 15-ID raw tomographic data and reconstruct using tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""
from pyhdf import SD
import os

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re

def main():

    file_name = '/local/dataraid/databank/APS_15_ID/AluminaStick_0A_fullRunRenamed/AluminaStick_.hdf'
    
    projections_start = 1
    projections_end = 361

    # to reconstruct a subset of slices set slices_start and slices_end
    # if omitted the full data set is recontructed
    slices_start = 800    
    slices_end = 804    

    mydata = dx.Import()

    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       projections_digits = 4,
                                                       data_type = 'hdf5',
                                                       log='INFO'
                                                       )

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    d.phase_retrieval(pixel_size=0.9e-4, dist=8.1, energy=17)
    #d.correct_drift()
    d.center=772.2
    d.gridrec()

    # Write to stack of TIFFs.
    mydata = ex.Export()
    mydata.xtomo_tiff(data = d.data_recon, output_file = 'tmp/AluminaStick_0A_', axis=0)

if __name__ == "__main__":
    main()


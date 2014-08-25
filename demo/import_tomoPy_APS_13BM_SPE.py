# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_13BM_SPE.py
   :platform: Unix
   :synopsis: Import APS 13-BM SPE files in data exchange.

Example on how to use the `series_of_images`_ module to read APS 13-BM SPE raw tomographic data and reconstruct using tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples
--------

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re


def main():
    # read a series of SPE
    file_name = '/local/dataraid/databank/APS_13_BM/SPE/run2_soln1_2_.SPE'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/APS_13_BM_SPE.h5'

    white_start = 1
    white_end = 8
    white_step = 2
    projections_start = 2
    projections_end = 7
    projections_step = 2

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 100    
    slices_end = 104    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_step = projections_step,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       projections_zeros=False,
                                                       white_zeros=False,
                                                       dark_zeros=False,
                                                       projections_digits = 1,
                                                       data_type='spe',
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
    d.center=705
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/APS_13_BM_SPE_', axis=0)

if __name__ == "__main__":
    main()


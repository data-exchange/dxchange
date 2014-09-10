# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_13BM_netCDF.py
   :platform: Unix
   :synopsis: Import APS 13-BM netCDF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 13-BM netCDF raw tomographic data and and reconstruct using tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re


def main():
    # read a series of netCDF
    file_name = '/local/dataraid/databank/APS_13_BM/NC/Dorthe_F_.nc'

    white_start = 1
    white_end = 4
    white_step = 2
    projections_start = 2
    projections_end = 3
    projections_step = 1

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 300    
    slices_end = 304    

    mydata = dx.Import()    
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_step = projections_step,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       projections_digits = 3,
                                                       data_type='nc',
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
    d.center=484.5
    d.gridrec()

    # Write to stack of TIFFs.
    mydata = ex.Export()
    mydata.xtomo_tiff(data = d.data_recon, output_file = 'tmp/APS_13_BM_netCDF_2_tomoPy_', axis=0)

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_2BM.py
   :platform: Unix
   :synopsis: Import APS 2-BM HDF4 files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 2-BM HDF4 raw tomographic data and reconstruct using tomoPy

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

from pyhdf import SD
import os

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re

def main():
    log_file = '/local/dataraid/databank/Sangid/Sam01/Sam01_exp.hdf'

    #Read APS 2-BM log file data
    f = SD.SD(log_file)

    sds = f.select('base_name')
    data = sds.get()
    base_name = ''.join(data)
    print base_name

    file_name = os.path.split(log_file)[0] + "/" + "raw" + "/" + base_name + "_.hdf"
     
    sds = f.select('start_angle')
    start_angle = sds.get()[0]

    sds = f.select('end_angle')
    end_angle = sds.get()[0]

    sds = f.select('angle_interval')
    angle_interval = sds.get()[0]

    sds = f.select('num_dark_fields')
    num_dark_fields = sds.get()[0]

    f.end()
    
    white_start = 1
    white_end = 2 
    projections_start = 2
    projections_end = projections_start + (int)((end_angle -  start_angle) / angle_interval) + 1
    dark_start = projections_end + 1 
    dark_end = dark_start + num_dark_fields

    sample_name = base_name

    # to reconstruct a subset of slices set slices_start and slices_end
    # if omitted the full data set is recontructed
    
    slices_start = 1365
    slices_end = 1369

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 5,
                                                       data_type = 'hdf4',
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
    d.center=1059.2
    d.gridrec()

    # Write to stack of TIFFs.
    mydata = ex.Export()
    mydata.xtomo_tiff(data = d.data_recon, output_file = 'tmp/APS_2_BM_hdf4_2_tomoPy_', axis=0)

if __name__ == "__main__":
    main()


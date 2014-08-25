# -*- coding: utf-8 -*-
"""
.. module:: convert_ALS_legacy.py
   :platform: Unix
   :synopsis: Convert ALS TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read ALS raw tomographic data and save them as Data Exchange

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


from pyhdf import SD
import os

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    log_file = '/local/dataraid/databank/Sangid/Sam01/Sam01_exp.hdf'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Sangid_ShortFiber.h5'

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

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 1000    
#    slices_end = 1004    
    
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                     projections_start = projections_start,
                                                     projections_end = projections_end,
                                                     white_start = white_start,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                     white_end = white_end,
                                                     dark_start = dark_start,
                                                     dark_end = dark_end,
                                                     projections_digits = 5,
                                                     data_type = 'hdf4',
                                                     log='INFO'
                                                     )
    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          sample_name = sample_name,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
.. module:: convert_Anka.py
   :platform: Unix
   :synopsis: Convert Anka TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read Anka TIFF raw tomographic data and save them as Data Exchange

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

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re

def main():

    file_name = '/local/dataraid/databank/Anka/radios/image_.tif'
    dark_file_name = '/local/dataraid/databank/Anka/darks/image_.tif'
    white_file_name = '/local/dataraid/databank/Anka/flats/image_.tif'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Anka.h5'

    projections_start = 0
    projections_end = 3167
    white_start = 0
    white_end = 100
    dark_start = 0
    dark_end = 100

    sample_name = 'Anka'
    
    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 800    
#    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       sample_name = sample_name,
                                                       projections_digits = 5,
                                                       log='INFO'
                                                       )

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )
    
if __name__ == "__main__":
    main()


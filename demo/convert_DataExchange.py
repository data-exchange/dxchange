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

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex


def main():

    file_name = '/media/DISK_01/databank/dataExchange/microCT/Elettra.h5'
    file_name_out = '/media/DISK_01/databank/dataExchange/microCT/Elettra_out.h5'

    
    # set to read all slices between slices_start and slices_end
    # if omitted all data set will be read   
#    slices_start = 150    
#    slices_end = 154    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       data_type='h5',
                                                       log='INFO'
                                                       )

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = file_name_out,
                          data_exchange_type = 'tomography_raw_projections')

if __name__ == "__main__":
    main()


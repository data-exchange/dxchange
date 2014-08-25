# -*- coding: utf-8 -*-
"""
.. module:: convert_Grenoble.py
   :platform: Unix
   :synopsis: Convert Grenoble Lab TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to Grenoble Lab TIFF raw tomographic data and save them as Data Exchange

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

def main():


    # HN-MR-002-1.0kPa/  HN-MR-002-2.0kPa/  HN-MR-002-3.0kPa/
##    file_name = '/local/dataraid/databank/GrenobleGranularData/Tomo/HN-MR-002-1_0kPa/Radios_original/HN-MR-002-SAT_.tif'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/HN-MR-002-SAT.h5'
##    sample_name = 'HN-MR-002-SAT'

    file_name = '/local/dataraid/databank/GrenobleGranularData/Tomo/HN-MR-002-2_0kPa/Radios_original/HN-MR-002-2KPA_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/HN-MR-002-2KPA.h5'
    sample_name = 'HN-MR-002-2KPA'

##    file_name = '/local/dataraid/databank/GrenobleGranularData/Tomo/HN-MR-002-3_0kPa/Radios_original/HN-MR-002-3_0KPA_.tif'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/HN-MR-002-3_0KPA.h5'
##    sample_name = 'HN-MR-002-3_0KPA'

    projections_start = 1
    projections_end = 1201

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 1000    
#    slices_end = 1004    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       sample_name = sample_name,
                                                       projections_digits = 5,
                                                       projections_zeros = True,
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


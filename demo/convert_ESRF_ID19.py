# -*- coding: utf-8 -*-
"""
.. module:: main_convert_esrf.py
   :platform: Unix
   :synopsis: Convert esrf ID-19 edf files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/ESRF/scan.edf'
    dark_file_name = '/local/dataraid/databank/ESRF/dark.edf'
    white_file_name = '/local/dataraid/databank/ESRF/flat.edf'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/ESRF_test_01.h5'

    sample_name = 'esrf'


    
    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 800    
    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       white_file_name = white_file_name,
                                                       dark_file_name = dark_file_name,
                                                       sample_name = sample_name,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       data_type='edf',
                                                       log='INFO'
                                                       )

##    mydata = ex.Export()
##    # Create minimal data exchange hdf5 file
##    mydata.xtomo_exchange(data = data,
##                          data_white = white,
##                          data_dark = dark,
##                          theta = theta,
##                          hdf5_file_name = hdf5_file_name,
##                          data_exchange_type = 'tomography_raw_projections'
##                          )
##    mydata = dx.Import()
##    # Create minimal hdf5 file
##    mydata.stack(file_name,
##                 hdf5_file_name = hdf5_file_name,
##                 white_file_name = white_file_name,
##                 dark_file_name = dark_file_name,
##                 projections_data_type = 'edf',
##                 white_data_type = 'edf',
##                 dark_data_type = 'edf',
##                 sample_name = sample_name,
##                 log='INFO'
##                 )

if __name__ == "__main__":
    main()


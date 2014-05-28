# -*- coding: utf-8 -*-
"""
.. module:: main_convert_Australian.py
   :platform: Unix
   :synopsis: Convert Australian Synchrotron facility TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/AS/Mayo_tooth_AS/SAMPLE_T_.tif'
    dark_file_name = '/local/dataraid/databank/AS/Mayo_tooth_AS/DF__AFTER_.tif'
    white_file_name = '/local/dataraid/databank/AS/Mayo_tooth_AS/BG__BEFORE_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Australian_test.h5'
    sample_name = 'Teeth'

    projections_start = 0
    projections_end = 1801
    white_start = 0
    white_end = 10
    white_step = 1
    dark_start = 0
    dark_end = 10
    dark_step = 1

    # to reconstruct slices from slices_start to slices_end
    # if omitted all data set is recontructed
    
    slices_start = 290    
    slices_end = 294    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       sample_name = sample_name,
                                                       projections_digits = 4,
                                                       white_digits = 2,
                                                       dark_digits = 2,
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


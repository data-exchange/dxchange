# -*- coding: utf-8 -*-
"""
.. module:: convert_VirginiaTech.py
   :platform: Unix
   :synopsis: Convert TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/VirginiaTech/test_sample_Diplo_4/Diplodocus_1_200mm_4_.tif'
    dark_file_name = '/local/dataraid/databank/VirginiaTech/test_sample_Diplo_4/Diplodocus_1_200mm_4postDark_.tif'
    white_file_name = '/local/dataraid/databank/VirginiaTech/test_sample_Diplo_4/Diplodocus_1_200mm_4postFlat_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/VirginiaTech_test.h5'
    sample_name = 'Diplodocus_1_200mm_'

    projections_start = 1 # projection 0 is dark so we skip it
    projections_end = 1500
    white_start = 0
    white_end = 10
    white_step = 1
    dark_start = 0
    dark_end = 10
    dark_step = 1

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 600    
    slices_end = 604    

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

